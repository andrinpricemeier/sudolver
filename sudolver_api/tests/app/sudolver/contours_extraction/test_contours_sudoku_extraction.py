from app.sudolver.contours_extraction.digit_classifier import DigitClassifier
from solvers.sudoku.sudoku_solver import SudokuSolver
from app.sudolver.contours_extraction.contours_sudoku_extraction import (
    ContoursSudokuExtraction,
)
from app.sudolver.image_rgb import ImageRGB


def load_classifier() -> DigitClassifier:
    model_path = "trained_model/svm-digit-classifier_v1.0.joblib"
    return DigitClassifier(model_path)


def load_extractor() -> ContoursSudokuExtraction:
    return ContoursSudokuExtraction(SudokuSolver(), load_classifier())


def load_image(filename):
    fullpath = f"tests/data/sudolver/{filename}"
    return ImageRGB.from_file(fullpath)


def test_solves_correctly():
    sudolver = load_extractor()
    test_image = load_image("sudoku_solvable.jpg")
    solution = sudolver.extract(test_image)
    assert solution is not None
