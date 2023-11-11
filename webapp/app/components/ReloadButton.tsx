import { RefreshIcon } from "@heroicons/react/solid";

export interface IReloadButton {
  onClick: () => void;
}

export const ReloadButton = (props: IReloadButton) => {
  return (
    <button
      onClick={props.onClick}
      className="place-self-center h-12 w-12 text-blue"
    >
      <RefreshIcon />
    </button>
  );
};
