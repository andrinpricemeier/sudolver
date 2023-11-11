import { TakeSnapshotButton } from "./TakeSnapshotButton";

export default {
  title: "Take Snapshot Button",
  component: TakeSnapshotButton,
};

const Template = (args: any) => <TakeSnapshotButton {...args} />;

export const Primary = Template.bind({}) as any;
Primary.args = {};
