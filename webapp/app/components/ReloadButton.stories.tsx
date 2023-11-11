import { ReloadButton } from "./ReloadButton";

export default {
  title: "Reload Button",
  component: ReloadButton,
};

const Template = (args: any) => <ReloadButton {...args} />;

export const Primary = Template.bind({}) as any;
Primary.args = {};
