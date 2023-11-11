from typing import List, Tuple
import traceback
from ..utils import laplacian
from .image_analysis import ImageAnalysis
from ..image_rgb import ImageRGB
from .image_table_extraction import ImageTableExtraction
from ..sudoku_extraction import SudokuExtraction
from solvers.sudoku.sudoku_solver import SudokuSolver


class TextractSudokuExtraction(SudokuExtraction):
    def __init__(
        self,
        solver: SudokuSolver,
        image_analysis: ImageAnalysis,
        table_extraction: ImageTableExtraction,
    ) -> None:
        self.solver = solver
        self.image_analysis = image_analysis
        self.table_extraction = table_extraction

    def extract(self, image: ImageRGB) -> Tuple[List[List[int]], List[List[str]]]:
        try:
            print("Trying AWS Textract based sudoku extraction/solving.")
            print("Sharpening image with a laplacian operator.")
            sharp = laplacian(image, alpha=10)
            print("Analysing image using AWS Textract.")
            analyzed = self.image_analysis.analyze(sharp.get_jpg_bytes())
            print("Extracting tables.")
            tables = self.table_extraction.extract_tables(analyzed)
            print("Retrieving first valid sudoku table.")
            sudoku_table = self.__get_first_valid_sudoku(tables)
            print("Solving sudoku using a constraint solver.")
            solution = self.solver.solve(sudoku_table)
            print("Successfully solved sudoku using AWS Textract.")
            return (solution, sudoku_table)
        except Exception as ex:
            print(repr(ex))
            print(traceback.format_exc())
            raise Exception("AWS Textract failed.")

    def __trim_table(self, table):
        new_table = []
        for row_index in range(len(table)):
            if row_index >= 9:
                break
            new_row = []
            new_table.append(new_row)
            for col_index in range(len(table[row_index])):
                if col_index >= 9:
                    break
                new_row.append(table[row_index][col_index])
        return new_table

    def __trim__tables(self, tables):
        new_tables = []
        for table in tables:
            new_tables.append(self.__trim_table(table))
        return new_tables

    def __is_valid_sudoku_table(self, table):
        if len(table) != 9:
            return False
        for row in table:
            if len(row) != 9:
                return False
        for row in table:
            for col in row:
                if len(col) > 0 and not col.isdigit():
                    return False
        return True

    def __get_first_valid_sudoku(self, tables):
        trimmed = self.__trim__tables(tables)
        for table in trimmed:
            if self.__is_valid_sudoku_table(table):
                return table
        return []
