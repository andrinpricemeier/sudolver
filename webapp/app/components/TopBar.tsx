export interface ITopBarProps {
  children: React.ReactNode;
}

export const TopBar = (props: ITopBarProps) => {
  return (
    <div className="p-5 flex justify-center gap-x-5 bg-black">
      {props.children}
    </div>
  );
};
