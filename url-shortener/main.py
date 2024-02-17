import pyshorteners
import qrcode
from qrcode.constants import ERROR_CORRECT_H

shortener = pyshorteners.Shortener()

def generate_personalized_link(long_url, keyword):
    try:
        short_url = shortener.tinyurl.short(long_url)
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=ERROR_CORRECT_H,
            box_size=10,
            border=5
        )
        qr.add_data(short_url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        img_path = f"{keyword}.png"
        img.save(img_path)
        
        return short_url, img_path
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None

if __name__ == "__main__":
    long_url = "https://www.yourwebsite.com/amazing-campaign"
    keyword = "summer-sale"
    short_url, qr_code_path = generate_personalized_link(long_url, keyword)

    if short_url and qr_code_path:
        print(f"Shortened URL: {short_url}")
        print(f"QR Code saved as: {qr_code_path}")
    else:
        print("Failed to generate the shortened URL and QR code.")
