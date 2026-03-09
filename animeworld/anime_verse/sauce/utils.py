import re
from django import template
from PIL import Image
import os

register = template.Library()

@register.filter
def youtube_embeded(url):
    pattern = r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]+)"
    match = re.search(pattern, url)

    if match:
        video_id = match.group(1)
        return f"https://www.youtube-nocookie.com/embed/{video_id}?autoplay=1"
    return url

# image to pdf
def image_to_pdf(image_files, output_path):
    images = []

    for image in image_files:
        img = Image.open(image)

        # Convert transparent images
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        images.append(img)

    if images:
        images[0].save(
            output_path,
            save_all=True,
            append_images=images[1:]
        )