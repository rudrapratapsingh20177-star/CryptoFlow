import requests
# CoinGecko API endpoint for fetching cryptocurrency prices
url = "https://api.coingecko.com/api/v3/simple/price" 
# Select the cryptocurrency 
params = {
    "ids": "bitcoin,ethereum,solana", 
    "vs_currencies": "inr"
}
print("============================================")
print("          CryptoFlow Price Tracker")
print("============================================")

try:
    # Send a GET request to the CoinGecko API
    response = requests.get(url, params=params, timeout=15)
    response.raise_for_status()  # Raise an error for bad responses
    data = response.json()  # Parse the JSON response

    # Extract prices for Bitcoin and Ethereum in INR
    bitcoin_price = data["bitcoin"]["inr"]
    ethereum_price = data["ethereum"]["inr"]
    solana_price = data["solana"]["inr"]

    # Display the prices
    print(f"\nBitcoin: Rs.{bitcoin_price:,.2f}")
    print(f"Ethereum: Rs.{ethereum_price:,.2f}")
    print(f"Solana: Rs.{solana_price:,.2f}")
    print("\nStatus: Prices fetched successfully!")
except requests.exceptions.RequestException as error:
    print("\nCould not fetch prices.")
    print("Check your internet connection or try again later.")
    print("Error:", error)
except (KeyError, ValueError) as error:
    print("\nThe API returned unexpected data.")
    print("Error:", error)