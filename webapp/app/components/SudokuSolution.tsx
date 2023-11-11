import { SudokuCell } from "./SudokuCell";

export type SudokuGrid = SudokuRow[];
export type SudokuRow = number[];
export type PrefilledGrid = PrefilledRow[];
export type PrefilledRow = string[];

export interface ISudokuSolutionProps {
  solution: [SudokuGrid, PrefilledGrid];
}

export const SudokuSolution = (props: ISudokuSolutionProps) => {
  console.log(props.solution);
  const sudokuSolution = props.solution[0];
  const prefilledGrid = props.solution[1];
  return (
    <table className="min-w-full">
      <tbody>
        {sudokuSolution.map((row: SudokuRow, rowIndex: number) => {
          return (
            <tr key={`sudoku.${rowIndex}`}>
              {row.map((cell: number, cellIndex: number) => {
                return (
                  <SudokuCell
                    key={`sudoku.${rowIndex}.${cellIndex}`}
                    prefilledValue={prefilledGrid[rowIndex][cellIndex]}
                    solution={cell}
                    rowIndex={rowIndex}
                    colIndex={cellIndex}
                  />
                );
              })}
            </tr>
          );
        })}
      </tbody>
    </table>
  );
};
