import { TopBar } from "./TopBar";
import { SudolverTitle } from "./SudolverTitle";

export default {
  title: "Top Bar",
  component: TopBar,
};

const Template = (args: any) => (
  <TopBar {...args}>
    <SudolverTitle />
  </TopBar>
);

export const Primary = Template.bind({}) as any;
Primary.args = {};
