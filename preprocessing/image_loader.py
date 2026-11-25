from datetime import datetime
from pathlib import Path

from PIL import Image


def load_images(path):
    images = []

    for file in Path(path).rglob("*"):
        if not file.is_file():
            continue

        if file.suffix.lower() not in (".png", ".jpg", ".jpeg"):
            continue

        timestamp = get_timestamp(file)
        if timestamp is None:
            continue

        images.append((file, timestamp))
        
    return images


def get_timestamp(image_path):
    with Image.open(image_path) as image:
        if not image.getexif():
            return None

        exif = image.getexif().get_ifd(34665)

        timestamp = exif.get(36867)
        subsec = exif.get(37521, "0")

        return datetime.strptime(
            f"{timestamp}.{subsec[:6]}",
            "%Y:%m:%d %H:%M:%S.%f"
        ).timestamp()


def sort_images(images):
    if not images:
        raise ValueError("No valid images found!")

    return sorted(images, key=lambda x: x[1])
    
