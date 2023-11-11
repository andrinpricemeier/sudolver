from typing import List
import traceback
from fastapi import APIRouter, Depends, HTTPException
from ..auth_middleware import perform_auth
from ..sudolver.sudolver import Sudolver
from ..sudolver.image_rgb import ImageRGB
from ..dependencies import sudolver_dependency
from pydantic import BaseModel

router = APIRouter()


class SudokuImage(BaseModel):
    image: str


class SudokuSolution(BaseModel):
    solution: List[List[int]]
    prefilled_table: List[List[str]]
    success: bool
    failure_reason: str


@router.get("/sudoku/smoketest")
async def sudoku_smoketest(sudolver: Sudolver = Depends(sudolver_dependency)):
    print("Smoke test passed.")
    return "Smoke test passed."


@router.post("/sudoku/analysis", response_model=SudokuSolution)
async def sudoku_analysis(
    sudoku_image: SudokuImage,
    sudolver: Sudolver = Depends(sudolver_dependency),
    _=Depends(perform_auth),  # Throw an error on authentication failure.
):
    try:
        print("Received request.")
        image_rgb: ImageRGB = ImageRGB.from_base64(sudoku_image.image)
        (solution, prefilled_table) = sudolver.solve(image_rgb)
        response = {}
        response["solution"] = solution
        response["prefilled_table"] = prefilled_table
        response["success"] = True
        response["failure_reason"] = "None"
        print("solution:")
        print(solution)
        print("prefilled board:")
        print(prefilled_table)
        print("Sudoku solved successfully.")
        return response
    except Exception as ex:
        print("Failed to solve sudoku. Returning failure.")
        print(repr(ex))
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(ex))
