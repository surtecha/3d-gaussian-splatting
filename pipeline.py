from preprocessing.image_loader import load_images, sort_images
from preprocessing.image_processing import extract_exif_metadata


def run_pipeline():
    image_directory = input("Image directory: ")
    images = load_images(image_directory)
    sorted_images = sort_images(images)

    metadata = extract_exif_metadata(sorted_images)

    