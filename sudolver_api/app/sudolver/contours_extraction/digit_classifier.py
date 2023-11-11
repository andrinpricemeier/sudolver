from typing import Optional
import numpy as np
from joblib import load
from skimage.feature import hog


class DigitClassifier:
    def __init__(self, model_path: str) -> None:
        self.classifier = load(model_path)

    def calculate_features_hog(self, images):
        return np.array([hog(image) for image in images])

    def predict(self, image_gray) -> Optional[int]:
        hog_features = self.calculate_features_hog([image_gray])
        recognized_digit = self.classifier.predict(hog_features)[0]
        if recognized_digit == 0:
            return None
        else:
            return recognized_digit
