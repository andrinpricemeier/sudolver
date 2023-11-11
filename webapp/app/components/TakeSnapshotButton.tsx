export interface ITakeSnapshotButton {
  onClick: () => void;
}

export const TakeSnapshotButton = (props: ITakeSnapshotButton) => {
  return (
    <button
      className="place-self-center bg-red h-20 w-20 rounded-full"
      onClick={props.onClick}
    />
  );
};
