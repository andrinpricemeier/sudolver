import numpy as np
import cv2
from .image_rgb import ImageRGB


def laplacian(image: ImageRGB, alpha=10) -> ImageRGB:
    image_bytes = image.get_bytes()
    normalized = image_bytes / 255.0
    laplacian = cv2.Laplacian(normalized, cv2.CV_64F)
    sharp = normalized - alpha * laplacian
    sharp[sharp > 1] = 1
    sharp[sharp < 0] = 0
    sharp = sharp * 255
    sharp = sharp.astype(np.uint8)
    return ImageRGB(sharp)


def perspective_transform(image_bytes, conjugates, output_size=640):
    output = np.float32(
        [
            [0, 0],
            [output_size - 1, 0],
            [output_size - 1, output_size - 1],
            [0, output_size - 1],
        ]
    )
    matrix = cv2.getPerspectiveTransform(conjugates, output)
    return cv2.warpPerspective(
        image_bytes,
        matrix,
        (output_size, output_size),
        cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(0, 0, 0),
    )


def pred_to_conjugates2(top_left, top_right, bottom_right, bottom_left):
    return np.float32([top_left, top_right, bottom_right, bottom_left])


def pred_to_conjugates(xmin, ymin, xmax, ymax):
    return np.float32([[xmin, ymin], [xmax, ymin], [xmax, ymax], [xmin, ymax]])
