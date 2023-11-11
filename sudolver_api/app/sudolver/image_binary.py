from typing import Any
import cv2
import numpy as np


class ImageBinary:
    def __init__(self, image_bytes) -> None:
        self.image_bytes = image_bytes

    def get_bytes(self) -> Any:
        return self.image_bytes

    def find_contours(self) -> Any:
        contours, _ = cv2.findContours(
            self.image_bytes, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )
        return contours

    def invert(self) -> Any:
        return ImageBinary(np.invert(self.get_bytes()))
