from ..utils import perspective_transform, pred_to_conjugates
from ..image_rgb import ImageRGB


class BoundingBox:
    def __init__(
        self, xmin: int, ymin: int, xmax: int, ymax: int, confidence: float
    ) -> None:
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        self.confidence = confidence

    def area(self) -> float:
        width = self.xmax - self.xmin
        height = self.ymax - self.ymin
        return width * height

    def extract(self, image_rgb: ImageRGB) -> ImageRGB:
        conjugates = pred_to_conjugates(
            self.xmin,
            self.ymin,
            self.xmax,
            self.ymax,
        )
        transformed_bytes = perspective_transform(image_rgb.get_bytes(), conjugates)
        return ImageRGB(transformed_bytes)
