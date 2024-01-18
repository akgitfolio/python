import asyncio
import aiohttp
import aiosmtplib
from email.message import EmailMessage
from bs4 import BeautifulSoup

async def get_artist_data(artist_url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(artist_url) as response:
                response.raise_for_status()
                artist_data = await response.text()
                soup = BeautifulSoup(artist_data, 'html.parser')
                name = soup.find('meta', {'name': 'artist-name'})['content']
                bio = soup.find('meta', {'name': 'artist-bio'})['content']
                return {"name": name, "bio": bio, "website": artist_url}
        except aiohttp.ClientError as e:
            raise Exception(f"Failed to fetch artist data from {artist_url}: {e}")

async def get_gallery_data(gallery_url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(gallery_url) as response:
                response.raise_for_status()
                gallery_data = await response.text()
                soup = BeautifulSoup(gallery_data, 'html.parser')
                name = soup.find('meta', {'name': 'gallery-name'})['content']
                email = soup.find('meta', {'name': 'gallery-email'})['content']
                return {"name": name, "email": email, "website": gallery_url}
        except aiohttp.ClientError as e:
            raise Exception(f"Failed to fetch gallery data from {gallery_url}: {e}")

def generate_email(artist_data, gallery_data):
    subject = f"Submission from {artist_data['name']}"
    body = f"""
    Dear {gallery_data['name']},

    My name is {artist_data['name']} and I am an artist specializing in {artist_data['bio']}. 
    I am interested in submitting my work to your gallery. You can view my portfolio at {artist_data['website']}.

    Thank you for your time and consideration.

    Best regards,
    {artist_data['name']}
    """
    return {"subject": subject, "body": body}

async def send_email(sender_email, sender_password, recipient_email, subject, body):
    message = EmailMessage()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject
    message.set_content(body)

    try:
        async with aiosmtplib.SMTP(hostname='smtp.example.com', port=465, use_tls=True) as smtp:
            await smtp.login(sender_email, sender_password)
            await smtp.send_message(message)
    except aiosmtplib.SMTPException as e:
        raise Exception(f"Failed to send email: {e}")

async def main():
    try:
        artist_data = await get_artist_data('https://example-artist.com')
        gallery_data = await get_gallery_data('https://example-gallery.com')
        email_content = generate_email(artist_data, gallery_data)
        await send_email('example@gmail.com', 'your_password_here', gallery_data['email'], email_content['subject'], email_content['body'])
    except Exception as e:
        print(f"An error occurred: {e}")

asyncio.run(main())
