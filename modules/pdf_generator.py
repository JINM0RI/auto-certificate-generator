# modules/pdf_generator.py
import os
from PIL import Image

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PDF_DIR = os.path.join(BASE_DIR, "output", "pdfs")

def image_to_pdf(image_path: str) -> str:
    os.makedirs(PDF_DIR, exist_ok=True)

    image = Image.open(image_path)

    # Convert to RGB (required for PDF)
    if image.mode != "RGB":
        image = image.convert("RGB")

    filename = os.path.splitext(os.path.basename(image_path))[0]
    pdf_path = os.path.join(PDF_DIR, f"{filename}.pdf")

    image.save(pdf_path, "PDF", resolution=100.0)

    print("✅ PDF created:", pdf_path)
    return pdf_path
