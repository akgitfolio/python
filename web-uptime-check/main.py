import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time


URL = "https://google.com"
CHECK_INTERVAL = 60
EMAIL_FROM = "your_email@example.com"
EMAIL_TO = "recipient_email@example.com"
SMTP_SERVER = "smtp.example.com"
SMTP_PORT = 587
SMTP_USERNAME = "your_email@example.com"
SMTP_PASSWORD = "your_password"


def send_notification(subject, message):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO
    msg["Subject"] = subject

    msg.attach(MIMEText(message, "plain"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_FROM, EMAIL_TO, text)
        server.quit()
        print(f"Notification sent: {subject}")
    except Exception as e:
        print(f"Failed to send notification: {e}")


def check_website(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Website {url} is UP.")
        else:
            print(f"Website {url} is DOWN. Status code: {response.status_code}")
            send_notification(
                f"Website Down: {url}",
                f"The website {url} is down. Status code: {response.status_code}",
            )
    except requests.RequestException as e:
        print(f"Website {url} is DOWN. Error: {e}")
        send_notification(
            f"Website Down: {url}", f"The website {url} is down. Error: {e}"
        )


if __name__ == "__main__":
    print(f"Starting website uptime checker for {URL}...")
    while True:
        check_website(URL)
        time.sleep(CHECK_INTERVAL)
