from modules.email_sender import send_certificate

send_certificate(
    receiver_email="srivathsan747@gmail.com",
    receiver_name="Test User",
    pdf_path="output/pdfs/Test User.pdf"
)
