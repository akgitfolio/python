import advanced_weather_fetcher as awf
from datetime import datetime, timedelta
import smtplib
import schedule
import time

api_key = "YOUR_API_KEY"
location = "London"
plant_type = "Tomato"
water_threshold = 0.3
sender_email = "your_email@example.com"
receiver_email = "recipient_email@example.com"
password = "your_password"

def get_weather_data():
    weather = awf.WeatherFetcher(api_key, location)
    current_data = weather.get_current_weather()
    forecast = weather.get_hourly_forecast(hours=24)
    return current_data, forecast

def should_water(current_data, forecast):
    current_precipitation = current_data.get("precipitation", 0)
    for hour in forecast:
        if hour.get("precipitation", 0) > 0.01:
            return False
    if current_precipitation > water_threshold:
        return False
    return True

def send_watering_notification(time):
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        message = f"Subject: Watering Alert for {plant_type}\n\nIt's time to water your {plant_type}! The optimal watering window is between {time.strftime('%H:%M')} and {(time + timedelta(minutes=30)).strftime('%H:%M')}."
        server.sendmail(sender_email, receiver_email, message)

def schedule_watering():
    current_data, forecast = get_weather_data()
    if should_water(current_data, forecast):
        watering_time = datetime.now() + timedelta(hours=1)
        schedule.every().day.at(watering_time.strftime("%H:%M")).do(send_watering_notification, watering_time)

if __name__ == "__main__":
    schedule_watering()
    while True:
        schedule.run_pending()
        time.sleep(1)
