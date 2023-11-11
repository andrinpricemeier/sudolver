export interface IErrorMessageProps {
  onClick: () => void;
}

export const ErrorMessage = (props: IErrorMessageProps) => {
  return (
    <div
      className="bg-black p-10 w-full h-full flex flex-col place-content-center place-items-center"
      aria-live="polite"
      aria-busy={true}
    >
      <h2 className="mb-5 text-blue font-bold">Couldn't solve the sudoku.</h2>
      <button
        onClick={props.onClick}
        className="bg-beige text-black p-3 rounded font-bold"
      >
        Try again
      </button>
    </div>
  );
};
