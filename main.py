from modules.sheet_reader import get_participants
from modules.certificate_generator import generate_certificate
from modules.pdf_generator import image_to_pdf
from modules.email_sender import send_certificate
import os

def main():
    participants = get_participants()

    if not participants:
        print("❌ No participants found")
        return

    print(f"🚀 Processing {len(participants)} participants...\n")

    for person in participants:
        name = person["name"]
        email = person["email"]

        print(f"🎓 Generating certificate for: {name}")

        # 1. Generate certificate image
        image_path = generate_certificate(name)

        # 2. Convert image to PDF
        pdf_path = image_to_pdf(image_path)

        # 3. Send email
        send_certificate(
            receiver_email=email,
            receiver_name=name,
            pdf_path=pdf_path
        )

        print(f"✅ Completed for {name}\n")

    print("🎉 ALL CERTIFICATES SENT SUCCESSFULLY")

if __name__ == "__main__":
    main()
