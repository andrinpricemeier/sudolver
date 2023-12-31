import { SudokuSolution } from "./SudokuSolution";

export default {
  title: "Sudoku Solution",
  component: SudokuSolution,
};

const Template = (args: any) => <SudokuSolution {...args} />;

export const Primary = Template.bind({}) as any;
Primary.args = {
  solution: [
    [
      [1, 2, 3, 4, 6, 7, 8, 9],
      [1, 2, 3, 4, 6, 7, 8, 9],
      [1, 2, 3, 4, 6, 7, 8, 9],
      [1, 6, 3, 4, 6, 7, 8, 9],
      [1, 9, 3, 4, 6, 7, 8, 9],
      [1, 1, 3, 4, 6, 7, 8, 9],
      [1, 5, 3, 4, 6, 7, 8, 9],
      [1, 6, 3, 4, 6, 7, 8, 9],
      [1, 4, 3, 4, 6, 7, 8, 9],
    ],
    [
      ["", "2", "3", "4", "6", "7", "8", "9"],
      ["", "2", "3", "", "6", "7", "8", "9"],
      ["", "2", "3", "", "6", "7", "8", "9"],
      ["", "2", "3", "", "6", "7", "8", "9"],
      ["", "2", "3", "", "6", "7", "8", "9"],
      ["", "2", "3", "", "6", "7", "8", "9"],
      ["", "2", "3", "", "6", "7", "8", "9"],
      ["", "2", "3", "4", "6", "7", "8", "9"],
      ["", "2", "3", "4", "6", "7", "8", "9"],
    ],
  ],
};
