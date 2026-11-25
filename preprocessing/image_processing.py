from PIL import Image


def extract_exif_metadata(sorted_images):
    metadata = []
    
    for image, timestamp in sorted_images:
        with Image.open(image) as img:
            exif = img.getexif()
            sub_exif = exif.get_ifd(34665)

            metadata.append({
                "image": image,
                "timestamp": timestamp,
                "width": img.width,
                "height": img.height,
                "focal_length": sub_exif.get(37386),
                "focal_length_35mm": sub_exif.get(41989),
                "orientation": exif.get(274),
                "exposure_time": sub_exif.get(33434),
                "f_number": sub_exif.get(33437),
                "iso": sub_exif.get(34855),
            })

    return metadata
        