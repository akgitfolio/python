import yagmail


sender_email = "your_email@gmail.com"
receiver_email = "receiver_email@gmail.com"
password = "your_password"


yag = yagmail.SMTP(user=sender_email, password=password)


yag.send(
    to=receiver_email,
    subject="Yagmail Test",
    contents="This is a test email sent using yagmail.",
    attachments="document.pdf",
)
