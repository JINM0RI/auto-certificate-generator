import os
import smtplib
from email.message import EmailMessage
from pathlib import Path
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def send_certificates(participants, subject, body, certificates_dir: Path):
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        raise ValueError("Email credentials not set in .env")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        for p in participants:
            name = p["name"]
            email = p["email"]

            pdf_path = certificates_dir / f"{name.replace(' ', '_')}.pdf"

            if not pdf_path.exists():
                print(f"⚠️ Certificate missing for {name}")
                continue

            msg = EmailMessage()
            msg["From"] = EMAIL_ADDRESS
            msg["To"] = email
            msg["Subject"] = subject

            personalized_body = body.replace("{name}", name)
            msg.set_content(personalized_body)

            with open(pdf_path, "rb") as f:
                msg.add_attachment(
                    f.read(),
                    maintype="application",
                    subtype="pdf",
                    filename=pdf_path.name
                )

            server.send_message(msg)

    return True
