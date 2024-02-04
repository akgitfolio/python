import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


smtp_server = "smtp.gmail.com"
port = 587
sender_email = "your_email@gmail.com"
receiver_email = "receiver_email@gmail.com"
password = input("Type your password and press enter:")


subject = "Email with Attachment"
body = "This is an email with attachment sent from Python."


message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject


message.attach(MIMEText(body, "plain"))


filename = "document.pdf"
with open(filename, "rb") as attachment:
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())


encoders.encode_base64(part)


part.add_header(
    "Content-Disposition",
    f"attachment; filename= {filename}",
)


message.attach(part)


context = ssl.create_default_context()
with smtplib.SMTP(smtp_server, port) as server:
    server.starttls(context=context)
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message.as_string())
