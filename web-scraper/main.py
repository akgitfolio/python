import requests
from bs4 import BeautifulSoup
from datetime import datetime
from simple_web_scraper import EmailNotifier, CsvExporter

stock_symbols = ["META", "AAPL", "AMZN", "NFLX", "GOOGL"]

data_points = {
    "current_price": "fin-streamer[data-field='regularMarketPrice']",
    "previous_close": "td[data-test='PREV_CLOSE-value'] span"
}

def is_growth_stock(stock_symbol):
    return stock_symbol in ["META", "AAPL", "AMZN", "GOOGL"]

for stock_symbol in stock_symbols:
    url = f"https://finance.yahoo.com/quote/{stock_symbol}"

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    data = {}
    for point, selector in data_points.items():
        element = soup.select_one(selector)
        if element:
            data[point] = element.text.strip()

    if is_growth_stock(stock_symbol):
        price_increase_threshold = 0.1
        price_decrease_threshold = -0.05
    else:
        price_increase_threshold = 0.05
        price_decrease_threshold = -0.02

    current_price = float(data["current_price"].replace(',', ''))
    previous_close = float(data["previous_close"].replace(',', ''))

    price_change = (current_price - previous_close) / previous_close

    if price_change >= price_increase_threshold or price_change <= price_decrease_threshold:
        notifier = EmailNotifier(
            sender_email="your_email@example.com",
            recipient_email="your_recipient_email@example.com",
            smtp_server="smtp.yourserver.com",
            smtp_port=587,
            smtp_username="your_username",
            smtp_password="your_password"
        )

        alert_message = f"Stock Alert for {stock_symbol}:\n\n" \
                        f"Current price: ${current_price}\n" \
                        f"Previous close: ${previous_close}\n" \
                        f"Price change: {price_change:.2%}"
        notifier.send_email(subject=f"{stock_symbol} Price Alert", message=alert_message)

        exporter = CsvExporter(filename=f"{stock_symbol}_price_data.csv")
        exporter.export_data({
            "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Current Price": current_price,
            "Previous Close": previous_close
        })
