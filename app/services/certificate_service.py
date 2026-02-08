from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
FONT_PATH = BASE_DIR / "fonts" / "Poppins-Bold.ttf"

def generate_certificate(name, template_path, output_path, x, y, font_size):
    image = Image.open(template_path).convert("RGB")
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype(str(FONT_PATH), font_size)

    draw.text((x, y), name, fill="black", font=font)

    image.save(output_path)
