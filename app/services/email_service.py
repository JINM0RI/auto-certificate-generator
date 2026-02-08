import os
import base64
import time
import requests
from pathlib import Path

RESEND_API_KEY = os.getenv("RESEND_API_KEY")
RESEND_URL = "https://api.resend.com/emails"


def send_certificates(participants, subject, body, certificates_dir):
    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json"
    }

    for p in participants:
        cert_path = Path(certificates_dir) / f"{p['name']}.pdf"

        if not cert_path.exists():
            print(f"[WARN] Certificate missing for {p['name']}")
            continue

        # Read & encode PDF
        with open(cert_path, "rb") as f:
            encoded_pdf = base64.b64encode(f.read()).decode("utf-8")

        payload = {
            "from": "Certificates <onboarding@resend.dev>",
            "to": [p["email"]],
            "subject": subject,
            "html": body,
            "attachments": [
                {
                    "filename": f"{p['name']}.pdf",
                    "content": encoded_pdf
                }
            ]
        }

        response = requests.post(RESEND_URL, headers=headers, json=payload)

        if response.status_code >= 400:
            print(
                f"[ERROR] Failed for {p['email']} | "
                f"Status: {response.status_code} | "
                f"Response: {response.text}"
            )
        else:
            print(f"[OK] Email sent to {p['email']}")

        # 🛑 RATE LIMIT (very important)
        time.sleep(1.2)
