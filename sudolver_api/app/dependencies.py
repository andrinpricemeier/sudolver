from functools import lru_cache
from typing import Optional
from pydantic import BaseSettings
from .auth import Authenticator
from .sudolver.contours_extraction.contours_sudoku_extraction import (
    ContoursSudokuExtraction,
)
from .sudolver.object_detection.largest_sudoku_object_detection import (
    LargestSudokuObjectDetection,
)
from .sudolver.object_detection.yolo_sudoku_object_detection import (
    YOLOSudokuObjectDetection,
)
from .sudolver.sudolver import Sudolver
from .sudolver.textract_extraction.image_analysis import ImageAnalysis
from .sudolver.textract_extraction.image_table_extraction import ImageTableExtraction
from .sudolver.textract_extraction.textract_sudoku_extraction import (
    TextractSudokuExtraction,
)
from .sudolver.contours_extraction.digit_classifier import DigitClassifier
from solvers.sudoku.sudoku_solver import SudokuSolver


class Settings(BaseSettings):
    yolo_trained_model_path: str
    yolo_library_path: str
    digit_classifier_model_path: str
    sudolver_api_key: str
    aws_access_key_id: Optional[str]
    aws_secret_access_key: Optional[str]
    aws_region: str = "eu-central-1"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


async def get_sudolver() -> Sudolver:
    settings = get_settings()
    yolo_od = YOLOSudokuObjectDetection(
        yolo_library_path=settings.yolo_library_path,
        yolo_trained_model_path=settings.yolo_trained_model_path,
    )
    largest_sudoku_od = LargestSudokuObjectDetection(yolo_od)
    solver = SudokuSolver()
    classifier = DigitClassifier(model_path=settings.digit_classifier_model_path)
    contours_extractor = ContoursSudokuExtraction(solver, classifier)
    textract_extractor = TextractSudokuExtraction(
        solver,
        ImageAnalysis(
            settings.aws_access_key_id,
            settings.aws_secret_access_key,
            settings.aws_region,
        ),
        ImageTableExtraction(),
    )
    sudolver = Sudolver(largest_sudoku_od)
    sudolver.add_extractor(contours_extractor)
    sudolver.add_extractor(textract_extractor)
    return sudolver


async def sudolver_dependency() -> Sudolver:
    return await get_sudolver()


async def authenticator_dependency() -> Authenticator:
    settings = get_settings()
    return Authenticator(settings.sudolver_api_key)
