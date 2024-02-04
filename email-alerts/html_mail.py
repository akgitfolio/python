import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


smtp_server = "smtp.gmail.com"
port = 587
sender_email = "your_email@gmail.com"
receiver_email = "receiver_email@gmail.com"
password = input("Type your password and press enter:")


subject = "HTML Email"
html = """\
<html>
  <body>
    <p>Hi,<br>
       This is a <b>test</b> email sent using <a href="https://www.python.org">Python</a>.
    </p>
  </body>
</html>
"""


message = MIMEMultipart("alternative")
message["Subject"] = subject
message["From"] = sender_email
message["To"] = receiver_email


message.attach(MIMEText(html, "html"))


context = ssl.create_default_context()
with smtplib.SMTP(smtp_server, port) as server:
    server.starttls(context=context)
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message.as_string())
