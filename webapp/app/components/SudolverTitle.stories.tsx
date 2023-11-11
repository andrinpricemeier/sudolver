import { SudolverTitle } from "./SudolverTitle";

export default {
  title: "Sudolver Title",
  component: SudolverTitle,
};

const Template = (args: any) => <SudolverTitle {...args} />;

export const Primary = Template.bind({}) as any;
Primary.args = {};
