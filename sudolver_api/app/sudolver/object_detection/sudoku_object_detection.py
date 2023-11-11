from typing import List

from .bounding_box import BoundingBox
from ..image_rgb import ImageRGB


class SudokuObjectDetection:
    def predict(self, image_rgb: ImageRGB, min_confidence=0.75) -> List[BoundingBox]:
        pass
