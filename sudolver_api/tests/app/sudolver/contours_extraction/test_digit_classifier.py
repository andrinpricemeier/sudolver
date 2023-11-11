from app.sudolver.contours_extraction.digit_classifier import DigitClassifier
import cv2


def load_classifier():
    model_path = "trained_model/svm-digit-classifier_v1.0.joblib"
    return DigitClassifier(model_path)


def load_image(filename):
    img = cv2.imread(f"tests/data/digit_classifier/{filename}")
    assert img is not None, "Loading digit classifier image failed."
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # The classifier has only been trained on 64x64 images thus the number of features
    # must coincide with that image size.
    return cv2.resize(img, dsize=(64, 64), interpolation=cv2.INTER_CUBIC)


# Even though the digit classifier library does testing of its own,
# it still makes sense to make a few quick sanity checks to see whether our wrapper works.
def test_correct_classification():
    classifier = load_classifier()
    test_image = load_image("digit_2.png")
    classified_number = classifier.predict(test_image)
    assert classified_number == 2


def test_no_number():
    classifier = load_classifier()
    test_image = load_image("digit_none.png")
    classified_number = classifier.predict(test_image)
    assert classified_number is None
