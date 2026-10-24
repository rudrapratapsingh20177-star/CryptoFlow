import requests
import csv
import time
from datetime import datetime
from pathlib import Path

# API URL
API_URL = "https://api.coingecko.com/api/v3/simple/price"

# Cryptocurrencies to track
PARAMS = {
    "ids": "bitcoin,ethereum,solana",
    "vs_currencies": "inr"
}

# CSV file location
CSV_FILE = Path(__file__).parent / "crypto_prices.csv"


def create_csv_file():
    """Create the CSV file and its headers if it does not exist."""
    if not CSV_FILE.exists():
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                "timestamp",
                "cryptocurrency",
                "price_inr"
            ])


def collect_prices():
    """Fetch cryptocurrency prices and save them to CSV."""
    response = requests.get(
        API_URL,
        params=PARAMS,
        timeout=20
    )

    response.raise_for_status()
    data = response.json()

    timestamp = datetime.now().astimezone().isoformat(
        timespec="seconds"
    )

    cryptocurrencies = {
        "bitcoin": "BTC",
        "ethereum": "ETH",
        "solana": "SOL"
    }

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        for coin_id, symbol in cryptocurrencies.items():
            price = data[coin_id]["inr"]

            writer.writerow([
                timestamp,
                symbol,
                price
            ])

    print(
        f"[{timestamp}] "
        f"BTC: Rs. {data['bitcoin']['inr']:,.2f} | "
        f"ETH: Rs. {data['ethereum']['inr']:,.2f} | "
        f"SOL: Rs. {data['solana']['inr']:,.2f}"
    )


def main():
    create_csv_file()

    print("CryptoFlow collector started!")
    print("Tracking Bitcoin, Ethereum, and Solana.")
    print("Collecting prices every 60 seconds.")
    print("Press Ctrl+C to stop the collector.\n")

    while True:
        wait_seconds = 60

        try:
            collect_prices()

        except requests.exceptions.HTTPError as error:
            if error.response is not None and error.response.status_code == 429:
                wait_seconds = 120
                print("\nAPI rate limit reached (429).")
                print("Waiting 2 minutes before retrying.\n")
            else:
                print(f"\nHTTP error: {error}")
                print("Will retry after 60 seconds.\n")

        except (
            requests.exceptions.RequestException,
            KeyError,
            ValueError
        ) as error:
            print(f"\nCould not collect prices: {error}")
            print("Will retry after 60 seconds.\n")

        except Exception as error:
            print(f"\nUnexpected error: {error}")
            print("Will retry after 60 seconds.\n")

        try:
            time.sleep(wait_seconds)
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nCryptoFlow collector stopped.")