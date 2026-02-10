import os
from email.message import EmailMessage
from typing import Optional

from dotenv import load_dotenv
import aiosmtplib

load_dotenv()

MAIL_HOST = os.getenv("MAIL_HOST", "smtp.mailtrap.io")
MAIL_PORT = int(os.getenv("MAIL_PORT", "587"))
MAIL_USER = os.getenv("MAIL_USER", "")
MAIL_PASS = os.getenv("MAIL_PASS", "")
MAIL_FROM = os.getenv("MAIL_FROM", "noreply@example.com")


async def send_email(
    to_email: str, subject: str, html_body: str, plain_body: Optional[str] = None
):
    message = EmailMessage()
    message["From"] = MAIL_FROM
    message["To"] = to_email
    message["Subject"] = subject
    if plain_body:
        message.set_content(plain_body)
    message.add_alternative(html_body, subtype="html")

    await aiosmtplib.send(
        message,
        hostname=MAIL_HOST,
        port=MAIL_PORT,
        username=MAIL_USER,
        password=MAIL_PASS,
        start_tls=True,
    )
