from typing import Any, List
import traceback
from .image_rgb import ImageRGB
from .sudoku_extraction import SudokuExtraction
from .object_detection.sudoku_object_detection import SudokuObjectDetection


class Sudolver:
    def __init__(self, object_detection: SudokuObjectDetection) -> None:
        self.object_detection = object_detection
        self.extractors: List[SudokuExtraction] = []

    def add_extractor(self, extractor: SudokuExtraction) -> None:
        self.extractors.append(extractor)

    def solve(self, image: ImageRGB) -> Any:
        print("Resizing image for object detection.")
        resized = image.resize(width=640, height=640)
        print("Detecting largest sudoku in image.")
        largest_sudokus = self.object_detection.predict(resized, min_confidence=0.75)
        if len(largest_sudokus) == 0:
            raise Exception("Failed to detect sudoku on image.")
        largest_sudoku = largest_sudokus[0]
        print("Cutting image to detected sudoku.")
        cut_out_sudoku = largest_sudoku.extract(resized)
        if len(self.extractors) == 0:
            raise Exception(
                "No extractors defined. Please add them before solving a sudoku."
            )
        print(
            f"Extracting and solving sudokus by going through {len(self.extractors)} extractors."
        )
        for extractor in self.extractors:
            try:
                return extractor.extract(cut_out_sudoku)
            except Exception as ex:
                print(traceback.format_exc())
                print(repr(ex))
        raise Exception(
            "All sudoku extractors failed to extract a valid sudoku from the given image."
        )
