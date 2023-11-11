from app.sudolver.object_detection.yolo_sudoku_object_detection import (
    YOLOSudokuObjectDetection,
)
from app.sudolver.image_rgb import ImageRGB


def load_object_detection() -> YOLOSudokuObjectDetection:
    model_path = "trained_model\\best_2022-04-09.pt"
    library_path = "yolov5"
    return YOLOSudokuObjectDetection(
        yolo_library_path=library_path, yolo_trained_model_path=model_path
    )


def load_image(filename) -> ImageRGB:
    fullpath = f"tests/data/sudoku_extractor/{filename}"
    return ImageRGB.from_file(fullpath).resize(width=640, height=640)


def test_correct_detection():
    object_detection = load_object_detection()
    test_image = load_image("sudoku_multiple.jpg")
    result = object_detection.predict(test_image)
    assert result is not None
