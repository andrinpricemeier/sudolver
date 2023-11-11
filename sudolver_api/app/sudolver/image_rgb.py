from typing import Any
import numpy as np
import cv2
import base64
import imgaug.augmenters as iaa
from .image_gray import ImageGray


class ImageRGB:
    def __init__(self, image_bytes) -> None:
        self.image_bytes = image_bytes

    def get_bytes(self) -> np.ndarray:
        return self.image_bytes

    def get_jpg_bytes(self) -> bytes:
        return cv2.imencode(".jpg", self.get_bytes())[1].tobytes()

    def resize(self, width: int, height: int) -> Any:
        aug = [iaa.CenterPadToSquare(), iaa.Resize({"height": height, "width": width})]
        seq = iaa.Sequential(aug)
        transformed_bytes = seq(image=self.image_bytes)
        return ImageRGB(transformed_bytes)

    def to_gray_image(self) -> ImageGray:
        gray_bytes = cv2.cvtColor(self.get_bytes(), cv2.COLOR_BGR2GRAY)
        return ImageGray(gray_bytes)

    def to_base64(self) -> str:
        _, buffer = cv2.imencode(".jpg", self.get_bytes())
        return base64.b64encode(buffer).decode("ascii")

    @classmethod
    def from_base64(class_type: Any, image_base64: str) -> Any:
        image_bytes = base64.b64decode(image_base64)
        jpg_as_np = np.frombuffer(image_bytes, dtype=np.uint8)
        decoded_bytes = cv2.imdecode(jpg_as_np, flags=1)
        return class_type(decoded_bytes)

    @classmethod
    def from_file(class_type: Any, fullpath: str) -> Any:
        bgr_bytes = cv2.imread(fullpath)
        rgb_bytes = cv2.cvtColor(bgr_bytes, cv2.COLOR_BGR2RGB)
        return class_type(rgb_bytes)
