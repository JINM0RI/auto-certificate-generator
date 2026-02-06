from PIL import Image, ImageDraw, ImageFont
import os

def generate_certificate(
    name: str,
    template_path: str,
    output_path: str,
    x: int,
    y: int,
    font_size: int
):
    image = Image.open(template_path).convert("RGB")
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype("fonts/Poppins-Bold.ttf", font_size)

    draw.text((x, y), name, fill="black", font=font)

    image.save(output_path)
