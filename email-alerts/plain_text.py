import smtplib


smtp_server = "smtp.gmail.com"
port = 587
sender_email = "your_email@gmail.com"
receiver_email = "receiver_email@gmail.com"
password = input("Type your password and press enter:")


subject = "Hi there"
body = "This message is sent from Python."

message = f"""\
Subject: {subject}

{body}
"""


context = ssl.create_default_context()
with smtplib.SMTP(smtp_server, port) as server:
    server.starttls(context=context)
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)
