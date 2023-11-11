from typing import List
from .sudoku_object_detection import SudokuObjectDetection
from ..image_rgb import ImageRGB
from .bounding_box import BoundingBox


class LargestSudokuObjectDetection(SudokuObjectDetection):
    def __init__(self, decorated: SudokuObjectDetection):
        self.decorated = decorated

    def find_largest_sudoku(self, found_sudokus: List[BoundingBox]):
        max_area = 0.0
        max_sudoku = None
        for sudoku in found_sudokus:
            if sudoku.area() > max_area:
                max_sudoku = sudoku
                max_area = sudoku.area()
        return max_sudoku

    def predict(self, image_rgb: ImageRGB, min_confidence=0.75) -> List[BoundingBox]:
        bounding_boxes = self.decorated.predict(image_rgb, min_confidence)
        largest_sudoku = self.find_largest_sudoku(bounding_boxes)
        if largest_sudoku is None:
            return []
        else:
            return [largest_sudoku]
