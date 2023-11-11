import { BottomBar } from "./BottomBar";
import { TakeSnapshotButton } from "./TakeSnapshotButton";
import { ReloadButton } from "./ReloadButton";

export default {
  title: "Bottom Bar",
  component: BottomBar,
};

const Template = (args: any) => (
  <BottomBar {...args}>
    <TakeSnapshotButton onClick={() => {}} />
    <ReloadButton onClick={() => {}} />
  </BottomBar>
);

export const Primary = Template.bind({}) as any;
Primary.args = {};
