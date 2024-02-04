from mailtrap import Mail, Address, MailtrapClient


mail = Mail(
    sender=Address(email="mailtrap@example.com", name="Mailtrap Test"),
    to=[Address(email="recipient@email.com", name="Recipient Name")],
    subject="Your HTML Email Subject Here",
    text="This is a fallback text for email clients that don't render HTML",
    html="""
    <!DOCTYPE html>
    <html>
    <head>
    <title>Email Title</title>
    </head>
    <body>
    <h1>Hello, World!</h1>
    <p>This is an <strong>HTML email</strong> sent from the Mailtrap Python SDK.</p>
    <p>Here's a link: <a href="https://example.com">Visit Example.com</a></p>
    </body>
    </html>
    """,
    category="HTML Email",
    headers={"X-Custom-Header": "Value"},
)


client = MailtrapClient(token="your-api-key")


client.send(mail)
print("HTML email sent successfully.")
