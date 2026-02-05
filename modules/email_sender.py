# modules/email_sender.py
import smtplib
import ssl
from email.message import EmailMessage
import os

def send_certificate(
    receiver_email: str,
    receiver_name: str,
    pdf_path: str
):
    sender_email = "srivathsan.r2003@gmail.com"
    app_password = "ylrb rvzr mymc nbtx"

    msg = EmailMessage()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = "Your Participation Certificate"

    msg.set_content(
        f"""
Hello {receiver_name},

Thank you for participating in our event.
Please find your certificate attached.

Best regards,
Event Team
"""
    )

    with open(pdf_path, "rb") as f:
        file_data = f.read()
        file_name = os.path.basename(pdf_path)

    msg.add_attachment(
        file_data,
        maintype="application",
        subtype="pdf",
        filename=file_name
    )

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, app_password)
        server.send_message(msg)

    print(f"✅ Email sent to {receiver_email}")
