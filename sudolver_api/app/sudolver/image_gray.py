from typing import Any
import cv2
from .image_binary import ImageBinary


class ImageGray:
    def __init__(self, image_bytes) -> None:
        self.image_bytes = image_bytes

    def apply_clahe(self, clip_limit, tile_size) -> Any:
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_size)
        return ImageGray(clahe.apply(self.image_bytes))

    def to_binary(
        self,
    ) -> ImageBinary:
        _, image_binary = cv2.threshold(
            self.image_bytes, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU
        )
        return ImageBinary(image_binary)
