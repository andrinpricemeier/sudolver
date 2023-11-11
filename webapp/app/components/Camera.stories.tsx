import { Camera } from "./Camera";

export default {
  title: "Camera",
  component: Camera,
};

const Template = (args: any) => <Camera snapshotTaken={() => {}} {...args} />;

export const Primary = Template.bind({}) as any;
Primary.args = {};
