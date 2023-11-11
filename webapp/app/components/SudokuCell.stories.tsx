import { SudokuCell } from "./SudokuCell";

export default {
  title: "Sudoku Cell",
  component: SudokuCell,
};

const Template = (args: any) => <SudokuCell {...args} />;

export const Primary = Template.bind({}) as any;
Primary.args = {
  solution: 5,
  prefilledValue: "",
};
