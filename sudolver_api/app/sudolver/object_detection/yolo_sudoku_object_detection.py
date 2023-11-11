from typing import List

from .sudoku_object_detection import SudokuObjectDetection
from ..image_rgb import ImageRGB
from .bounding_box import BoundingBox
import torch


class YOLOSudokuObjectDetection(SudokuObjectDetection):
    def __init__(self, yolo_library_path: str, yolo_trained_model_path: str):
        self.model = torch.hub.load(
            yolo_library_path,
            "custom",
            path=yolo_trained_model_path,
            source="local",
        )

    def find_largest_sudoku(self, found_sudokus: List[BoundingBox]):
        max_area = 0.0
        max_sudoku = None
        for sudoku in found_sudokus:
            if sudoku.area() > max_area:
                max_sudoku = sudoku
                max_area = sudoku.area()
        return max_sudoku

    def to_bounding_boxes(self, yolo_results) -> List[BoundingBox]:
        # Yes, df is a very generic name, but that's a name everyone knows when working with pandas.
        df = yolo_results.pandas().xyxy[0]
        bounding_boxes = []
        for _, row in df.iterrows():
            xmin, ymin, xmax, ymax, confidence = (
                int(row.xmin),
                int(row.ymin),
                int(row.xmax),
                int(row.ymax),
                float(row.confidence),
            )
            bounding_box = BoundingBox(xmin, ymin, xmax, ymax, confidence)
            bounding_boxes.append(bounding_box)
        return bounding_boxes

    def remove_low_confidence_boxes(
        self, boxes: List[BoundingBox], min_confidence=0.75
    ) -> List[BoundingBox]:
        return [box for box in boxes if box.confidence >= min_confidence]

    def predict(self, image_rgb: ImageRGB, min_confidence=0.75) -> List[BoundingBox]:
        print("Detecting sudoku using YOLO.")
        yolo_results = self.model(image_rgb.get_bytes())
        bounding_boxes = self.to_bounding_boxes(yolo_results)
        print(f"Found {len(bounding_boxes)} sudokus in the image.")
        print(f"Filtering sudokus by confidence: {min_confidence}.")
        filtered_boxes = self.remove_low_confidence_boxes(
            bounding_boxes, min_confidence
        )
        print(f"{len(filtered_boxes)} remained after filtering sudokus by confidence.")
        return filtered_boxes
