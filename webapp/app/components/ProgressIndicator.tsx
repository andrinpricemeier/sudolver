import { JellyTriangle } from "@uiball/loaders";

export const ProgressIndicator = () => {
  return (
    <div
      className="bg-black p-10 w-full h-full flex flex-col place-content-center place-items-center"
      aria-live="polite"
      aria-busy={true}
    >
      <h2 className="mb-5 text-blue font-bold">Solving your sudoku...</h2>
      <JellyTriangle color="#3497c6" />
    </div>
  );
};
