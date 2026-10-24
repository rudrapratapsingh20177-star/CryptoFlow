
# CryptoFlow 🚀

A real-time cryptocurrency price monitoring pipeline built with Python. It collects cryptocurrency prices, detects unusual price movements, and displays results on an interactive dashboard.

## Features

- Fetches Bitcoin (BTC), Ethereum (ETH), and Solana (SOL) prices in INR.
- Collects price data at regular intervals.
- Stores collected data in a CSV file.
- Detects price changes of 2% or more between consecutive readings.
- Displays current prices and percentage changes.
- Provides an interactive dashboard with charts and anomaly alerts.
- Automatically refreshes the dashboard every 60 seconds.

## Technologies Used

- Python
- Pandas
- Streamlit
- CoinGecko API
- CSV
- Git and GitHub

## Project Structure

```text
CryptoFlow/
├── main.py
├── collector.py
├── anomaly_detector.py
├── dashboard.py
├── .gitignore
├── README.md
└── crypto_prices.csv  # Generated locally
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/rudrapratapsingh20177-star/CryptoFlow.git
cd CryptoFlow
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install streamlit streamlit-autorefresh pandas requests
```

### 4. Collect cryptocurrency prices

In your first terminal, run:

```bash
python collector.py
```

Keep this terminal running to collect price data.

### 5. Launch the dashboard

Open a second terminal, activate the virtual environment, and run:

```bash
python -m streamlit run dashboard.py
```

The dashboard will open in your browser.

## Anomaly Detection

CryptoFlow flags price movements of 2% or more between consecutive recorded prices for each cryptocurrency. This is a simple rule-based alert, not a prediction of future prices.

## Future Improvements

- Integrate Apache Kafka for streaming data.
- Use Apache Spark for large-scale processing.
- Add Apache Airflow for workflow scheduling.
- Store historical prices in a database.
- Add automated tests and deployment.

## Author

Rudra Pratap Singh

GitHub: https://github.com/rudrapratapsingh20177-star
