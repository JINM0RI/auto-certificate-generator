import os
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

TEMPLATE_PATH = os.path.join(BASE_DIR, "templates", "certificate.png")
FONT_PATH = os.path.join(BASE_DIR, "fonts", "Poppins-Bold.ttf")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

def generate_certificate(name):
    print("FONT PATH:", FONT_PATH)
    print("FONT EXISTS:", os.path.exists(FONT_PATH))

    image = Image.open(TEMPLATE_PATH)
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype(FONT_PATH, 60)
    except OSError:
        print("⚠ Font failed, using default")
        font = ImageFont.load_default()

    text_x, text_y = 500, 300
    draw.text((text_x, text_y), name, fill="black", font=font)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, f"{name}.png")
    image.save(output_path)

    # print("✅ Certificate generated:", output_path)
    return output_path
