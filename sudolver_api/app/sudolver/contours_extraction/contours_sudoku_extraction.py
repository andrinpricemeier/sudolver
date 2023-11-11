from itertools import product
from typing import List, Tuple

from ..sudoku_extraction import SudokuExtraction
from ..image_binary import ImageBinary
from ..image_gray import ImageGray
from ..image_rgb import ImageRGB
import cv2
from .digit_classifier import DigitClassifier
from solvers.sudoku.sudoku_solver import SudokuSolver
from scipy.spatial import ConvexHull
import numpy as np
from ..utils import pred_to_conjugates2, perspective_transform


class ContoursSudokuExtraction(SudokuExtraction):
    def __init__(
        self,
        solver: SudokuSolver,
        digit_classifier: DigitClassifier,
    ) -> None:
        self.solver = solver
        self.digit_classifier = digit_classifier

    def extract(self, image: ImageRGB) -> Tuple[List[List[int]], List[List[str]]]:
        print("Trying contours based sudoku extraction/solving.")
        gray = image.to_gray_image()
        res = self.get_sudoku_bounding_boxes(gray)
        if res is not None:
            (bbs, image_binary) = res
            points = []
            for bb in bbs:
                x_center = bb[0] + bb[4]
                y_center = bb[1] + bb[5]
                points.append([x_center, y_center, bb])
            board = self.assign_board(points)
            kernels = [1, 3, 5, 7]
            for kernel in kernels:
                board_template = self.extract_numbers(board, image_binary, kernel)
                try:
                    solution = self.solver.solve(board_template)
                    print(
                        "Successfully solved sudoku using the contours based approach."
                    )
                    return (solution, board_template)
                except Exception:
                    # It's okay to ignore the errors here since
                    # we're iterating over all possible kernels.
                    # It only counts as a failure if all kernels fail.
                    pass
        raise Exception("Failed to solve sudoku using the contours based approach.")

    def find_corner(self, points):
        corner = None
        corner_dist = 0
        for i in range(len(points)):
            point = points[i]
            dist = np.linalg.norm(np.array([0, 0]) - np.array([point[0], point[1]]))
            if corner is None:
                corner = point
                corner_dist = dist
            elif dist < corner_dist:
                corner = point
                corner_dist = dist
        return corner

    def find_uppers(self, points, n):
        distances = []
        for i in range(len(points)):
            point = points[i]
            dist = np.linalg.norm(
                np.array([point[0], 0]) - np.array([point[0], point[1]])
            )
            distances.append(dist)
        mins = np.argsort(distances)
        output = []
        for i in range(n):
            output.append(points[mins[i]])
        return output

    def find_lefters(self, points, n):
        distances = []
        for i in range(len(points)):
            point = points[i]
            dist = np.linalg.norm(
                np.array([0, point[1]]) - np.array([point[0], point[1]])
            )
            distances.append(dist)
        mins = np.argsort(distances)
        output = []
        for i in range(n):
            output.append(points[mins[i]])
        return output

    def assign_border(self, board, points, n, row, col):
        corner = self.find_corner(points)
        uppers = self.find_uppers(points, n=n)
        lefters = self.find_lefters(points, n=n)
        board[row][col] = corner
        up_sorted = sorted(uppers, key=lambda p: p[0])
        left_sorted = sorted(lefters, key=lambda p: p[1])
        for i in range(n):
            up = up_sorted[i]
            if up != corner:
                board[row][col + i] = up
                points.remove(up)
        for i in range(n):
            left = left_sorted[i]
            if left != corner:
                board[row + i][col] = left
                points.remove(left)
        points.remove(corner)

    def assign_board(self, points):
        board = []
        for i in range(9):
            row = []
            board.append(row)
            for j in range(9):
                row.append(0)
        n = 9
        row = 0
        col = 0
        for cur in range(n - 1):
            current_n = n - cur
            self.assign_border(board, points, current_n, row, col)
            row += 1
            col += 1
        board[8][8] = points[0]
        return board

    def extract_numbers(self, board, image_binary: ImageBinary, kernel=1):
        board_template = []
        i = 0
        for row in board:
            template_row: List[str] = []
            board_template.append(template_row)
            j = 0
            for cell in row:
                bb = cell[2]
                conjugates = pred_to_conjugates2(
                    [bb[0], bb[1]], [bb[2], bb[1]], [bb[2], bb[3]], [bb[0], bb[3]]
                )
                binary_image = perspective_transform(
                    image_binary.get_bytes(), conjugates, output_size=64
                )
                gray_image = ImageGray(binary_image)
                binary_image = gray_image.to_binary()
                inverted_image: ImageBinary = binary_image.invert()
                open_kernel = cv2.getStructuringElement(
                    cv2.MORPH_ELLIPSE, (kernel, kernel)
                )
                opened = np.invert(
                    cv2.morphologyEx(
                        inverted_image.get_bytes(), cv2.MORPH_OPEN, open_kernel
                    )
                )
                digit = self.digit_classifier.predict(opened)
                if digit is None:
                    template_row.append("")
                else:
                    template_row.append(f"{digit}")
                j += 1
            i += 1
        return board_template

    def sudoku_cell_contours_to_bounding_boxes(self, cell_contours):
        # Format of bounding box: (xmin, xmax, ymin, ymax, width, height)
        bounding_boxes = []
        for contour in cell_contours:
            xmin, ymin, width, height = cv2.boundingRect(contour)
            bounding_box = (xmin, ymin, xmin + width, ymin + height, width, height)
            bounding_boxes.append(bounding_box)
        return bounding_boxes

    def get_contour_precedence(self, bounding_box):
        tolerance_factor = 10
        return (
            (bounding_box[1] // tolerance_factor) * tolerance_factor
        ) * 9 + bounding_box[0]

    def sort_bounding_boxes(self, bounding_boxes):
        sorted_boxes = bounding_boxes.copy()
        sorted_boxes.sort(key=lambda x: self.get_contour_precedence(x))
        return sorted_boxes

    def to_grid(self, bounding_boxes):
        sorted_boxes = self.sort_bounding_boxes(bounding_boxes)
        grid = []
        cell_index = 0
        for _ in range(9):
            row = []
            grid.append(row)
            for _ in range(9):
                row.append(sorted_boxes[cell_index])
                cell_index += 1
        return np.array(grid)

    def filter_valid_sudoku_cells(self, contours, min_cell_area=1000):
        cell_contours = []
        for i in range(len(contours)):
            hull = cv2.convexHull(contours[i])
            if len(contours[i]) < 125 and len(hull) > 3:
                hull_volume = ConvexHull(hull[:, 0, :]).volume
                if hull_volume > min_cell_area:
                    cell_contours.append(contours[i])
        return cell_contours

    def is_valid_sudoku(self, bounding_boxes):
        valid_boxes = []
        for bounding_box in bounding_boxes:
            width = bounding_box[4]
            valid_width = width >= 45 and width <= 125
            height = bounding_box[5]
            valid_height = height >= 45 and height <= 125
            if valid_width and valid_height:
                valid_boxes.append(bounding_box)
        if len(valid_boxes) == 81:
            return valid_boxes
        else:
            return None

    def get_sudoku_bounding_boxes(self, image_gray: ImageGray):
        clips = [2, 3, 4, 6, 8, 10]
        tiles = [(4, 4), (5, 5), (6, 6), (8, 8)]
        hyperparameters = product(clips, tiles)
        for (clip, tile) in hyperparameters:
            equalized: ImageGray = image_gray.apply_clahe(clip, tile)
            binary_image = equalized.to_binary()
            contours = binary_image.find_contours()
            cell_contours = self.filter_valid_sudoku_cells(contours)
            bounding_boxes = self.sudoku_cell_contours_to_bounding_boxes(cell_contours)
            bounding_boxes = self.is_valid_sudoku(bounding_boxes)
            if bounding_boxes is not None:
                return (bounding_boxes, binary_image)
        return None
