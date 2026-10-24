import pandas as pd
from pathlib import Path

# Find the CSV file in the project folder
CSV_FILE = Path(__file__).parent / "crypto_prices.csv"

# Price change threshold in percentage
THRESHOLD = 2.0


def detect_anomalies():
    # Check whether the CSV file exists
    if not CSV_FILE.exists():
        print("CSV file not found. Run collector.py first.")
        return

    # Read collected cryptocurrency prices
    df = pd.read_csv(CSV_FILE)

    # Check whether there is enough data
    if df.empty:
        print("No price data available yet.")
        return

    # Convert timestamp to datetime
    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        errors="coerce"
    )

    # Sort prices by cryptocurrency and time
    df = df.dropna(subset=["timestamp", "price_inr"])
    df = df.sort_values(["cryptocurrency", "timestamp"])

    # Calculate percentage change for each cryptocurrency
    df["change_percent"] = (
        df.groupby("cryptocurrency")["price_inr"]
        .pct_change() * 100
    )

    # Find price movements greater than the threshold
    anomalies = df[
        df["change_percent"].abs() >= THRESHOLD
    ]

    print("\n===== CryptoFlow Anomaly Detector =====")

    if anomalies.empty:
        print("No unusual price movements detected.")
    else:
        print("\nUnusual price movements found:\n")

        for _, row in anomalies.iterrows():
            direction = (
                "increased"
                if row["change_percent"] > 0
                else "decreased"
            )

            print(f"Coin: {row['cryptocurrency']}")
            print(f"Time: {row['timestamp']}")
            print(f"Price: Rs. {row['price_inr']:,.2f}")
            print(
                f"Change: {row['change_percent']:.2f}% "
                f"({direction})"
            )
            print("-" * 35)


if __name__ == "__main__":
    detect_anomalies()