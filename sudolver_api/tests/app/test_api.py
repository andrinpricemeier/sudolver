from fastapi.testclient import TestClient
from app.main import app
from app.sudolver.image_rgb import ImageRGB

client = TestClient(app)


def load_image(filename) -> ImageRGB:
    fullpath = f"tests/data/api/{filename}"
    return ImageRGB.from_file(fullpath)


def test_successful_solving():
    image = load_image("sudoku_solvable.jpg")
    image_base64 = image.to_base64()
    response = client.post(
        "/sudoku/analysis", json={"image": image_base64}, headers={"x-api-key": "DUMMY"}
    )
    sudoku_solution = response.json()
    assert response.status_code == 200
    assert sudoku_solution is not None
    assert sudoku_solution["solution"] is not None
    assert sudoku_solution["success"]
    assert sudoku_solution["failure_reason"] == "None"


def test_wrong_api_key():
    image = load_image("sudoku_solvable.jpg")
    image_base64 = image.to_base64()
    response = client.post(
        "/sudoku/analysis",
        json={"image": image_base64},
        headers={"x-api-key": "WRONG_KEY"},
    )
    assert response.status_code == 401


def test_missing_api_key_header():
    image = load_image("sudoku_solvable.jpg")
    image_base64 = image.to_base64()
    # Note: the x-api key header is missing - on purpose.
    response = client.post("/sudoku/analysis", json={"image": image_base64})
    assert response.status_code == 401
