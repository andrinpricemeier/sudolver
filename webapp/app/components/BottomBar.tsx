export interface IBottomBarProps {
  children: React.ReactNode;
}

export const BottomBar = (props: IBottomBarProps) => {
  return (
    <div className="p-5 grid grid-cols-3 bg-black">
      <div className="w-full" />
      {props.children}
    </div>
  );
};
