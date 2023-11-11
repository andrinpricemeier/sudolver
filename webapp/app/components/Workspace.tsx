export interface IWorkspaceProps {
  children: React.ReactNode;
}

export const Workspace = (props: IWorkspaceProps) => {
  return (
    <div className="bg-black grow flex justify-center">{props.children}</div>
  );
};
