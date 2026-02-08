import os
import requests
from pathlib import Path

RESEND_API_KEY = os.getenv("RESEND_API_KEY")

def send_certificates(participants, subject, body, certificates_dir):
    for p in participants:
        cert_path = Path(certificates_dir) / f"{p['name']}.pdf"

        with open(cert_path, "rb") as f:
            response = requests.post(
                "https://api.resend.com/emails",
                headers={
                    "Authorization": f"Bearer {RESEND_API_KEY}"
                },
                files={
                    "attachments[0]": f
                },
                data={
                    "from": "Certificates <onboarding@resend.dev>",
                    "to": p["email"],
                    "subject": subject,
                    "html": body
                }
            )

        response.raise_for_status()
