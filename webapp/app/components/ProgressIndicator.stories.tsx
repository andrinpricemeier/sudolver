import { ProgressIndicator } from "./ProgressIndicator";

export default {
  title: "Progress Indicator",
  component: ProgressIndicator,
};

const Template = (args: any) => <ProgressIndicator {...args} />;

export const Primary = Template.bind({}) as any;
Primary.args = {};
