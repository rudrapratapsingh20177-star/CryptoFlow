
import streamlit as st
import pandas as pd
from pathlib import Path
from streamlit_autorefresh import st_autorefresh

# -------------------------------
# Page configuration
# -------------------------------
st.set_page_config(
    page_title="CryptoFlow Dashboard",
    page_icon="📈",
    layout="wide"
)

# Automatically refresh every 60 seconds
st_autorefresh(
    interval=60_000,
    key="crypto_dashboard_refresh"
)

st.title("🚀 CryptoFlow: Crypto Price Dashboard")
st.caption("Live cryptocurrency monitoring with anomaly alerts")

# -------------------------------
# Load CSV data
# -------------------------------
CSV_FILE = Path(__file__).parent / "crypto_prices.csv"

if not CSV_FILE.exists():
    st.warning("No price data found yet. Start collector.py first.")
    st.stop()

try:
    df = pd.read_csv(CSV_FILE)
except pd.errors.EmptyDataError:
    st.warning("The CSV file is empty. Waiting for price data...")
    st.stop()

required_columns = {"timestamp", "cryptocurrency", "price_inr"}

if not required_columns.issubset(df.columns):
    st.error(
        "CSV columns are incorrect. Expected: "
        "timestamp, cryptocurrency, price_inr"
    )
    st.stop()

if df.empty:
    st.warning("No price records available yet.")
    st.stop()

# Clean and prepare data
df["timestamp"] = pd.to_datetime(
    df["timestamp"], errors="coerce"
)
df["price_inr"] = pd.to_numeric(
    df["price_inr"], errors="coerce"
)
df["cryptocurrency"] = (
    df["cryptocurrency"].astype(str).str.upper()
)

df = df.dropna(
    subset=["timestamp", "cryptocurrency", "price_inr"]
)

if df.empty:
    st.warning("No valid price records found.")
    st.stop()

df = df.sort_values("timestamp")

# -------------------------------
# Latest prices
# -------------------------------
st.subheader("💰 Latest Crypto Prices")

coins = ["BTC", "ETH", "SOL"]
columns = st.columns(3)

for column, coin in zip(columns, coins):
    coin_data = df[df["cryptocurrency"] == coin].sort_values(
        "timestamp"
    )

    with column:
        if coin_data.empty:
            st.metric(label=coin, value="No data")
            continue

        latest_price = coin_data.iloc[-1]["price_inr"]

        # Compare latest price with the previous recorded price
        if len(coin_data) >= 2:
            previous_price = coin_data.iloc[-2]["price_inr"]

            if previous_price != 0:
                change_percent = (
                    (latest_price - previous_price)
                    / previous_price
                ) * 100
            else:
                change_percent = None
        else:
            change_percent = None

        if change_percent is None:
            st.metric(
                label=f"{coin} Price",
                value=f"₹{latest_price:,.2f}",
                delta="Waiting for next reading"
            )
        else:
            st.metric(
                label=f"{coin} Price",
                value=f"₹{latest_price:,.2f}",
                delta=f"{change_percent:+.2f}%"
            )

# -------------------------------
# Percentage change chart
# -------------------------------
st.divider()
st.subheader("📊 Price Change Over Time")

chart_df = df.copy()

chart_df = chart_df.sort_values(
    ["cryptocurrency", "timestamp"]
)

chart_df["change_percent"] = (
    chart_df.groupby("cryptocurrency")["price_inr"]
    .transform(lambda prices: (prices / prices.iloc[0] - 1) * 100)
)

chart_data = chart_df.pivot_table(
    index="timestamp",
    columns="cryptocurrency",
    values="change_percent",
    aggfunc="last"
)

if not chart_data.empty:
    st.line_chart(chart_data)
    st.caption(
        "This chart shows percentage change from each coin's "
        "first recorded price."
    )

# -------------------------------
# Anomaly detection
# -------------------------------
st.divider()
st.subheader("🚨 Anomaly Alerts")

alerts_found = False

for coin in coins:
    coin_data = df[
        df["cryptocurrency"] == coin
    ].sort_values("timestamp").copy()

    if len(coin_data) < 2:
        continue

    coin_data["change_percent"] = (
        coin_data["price_inr"].pct_change() * 100
    )

    anomalies = coin_data[
        coin_data["change_percent"].abs() >= 2
    ]

    if not anomalies.empty:
        alerts_found = True

        for _, row in anomalies.tail(5).iterrows():
            direction = (
                "increased"
                if row["change_percent"] > 0
                else "decreased"
            )

            st.warning(
                f"{coin}: Price {direction} by "
                f"{abs(row['change_percent']):.2f}% "
                f"at {row['timestamp']}"
            )

if not alerts_found:
    st.success(
        "No anomalies detected. "
        "Alerts appear when a price changes by 2% or more."
    )

# -------------------------------
# Raw data
# -------------------------------
st.divider()

with st.expander("📁 View Collected Price Records"):
    st.dataframe(
        df.sort_values("timestamp", ascending=False),
        use_container_width=True
    )

st.caption(
    "CryptoFlow refreshes every 60 seconds. "
    "Keep collector.py running to collect new prices."
)
