import base64
from io import BytesIO

from PIL import Image


def encode_image_bytes(image: Image.Image):
    buffer = BytesIO()
    image.save(buffer, format="JPEG", quality=95)
    return buffer.getvalue()


def decode_image_bytes(image_bytes: bytes) -> Image.Image:
    image = Image.open(BytesIO(image_bytes))
    return image
