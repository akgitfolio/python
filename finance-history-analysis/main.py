import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt


def fetch_finance_data(symbol, start_date, end_date):
    try:

        stock_data = yf.download(symbol, start=start_date, end=end_date)
        return stock_data
    except Exception as e:
        print("Failed to fetch data:", e)
        return None


def analyze_finance_data(stock_data):
    if stock_data is not None:

        print("Summary Statistics:")
        print(stock_data.describe())

        stock_data["Close"].plot(figsize=(10, 5), grid=True)
        plt.title("Closing Price")
        plt.xlabel("Date")
        plt.ylabel("Price ($)")
        plt.show()
    else:
        print("No data to analyze.")


def generate_finance_report(stock_data):
    if stock_data is not None:

        stock_data.to_csv("stock_data.csv")
        print("Data saved to stock_data.csv")
    else:
        print("No data to generate report.")


def main():
    symbol = "AAPL"
    start_date = "2020-01-01"
    end_date = "2021-01-01"

    stock_data = fetch_finance_data(symbol, start_date, end_date)
    analyze_finance_data(stock_data)
    generate_finance_report(stock_data)


if __name__ == "__main__":
    main()
