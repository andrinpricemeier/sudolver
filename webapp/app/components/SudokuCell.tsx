import { useMemo, useState } from "react";

export interface ISudokuCellProps {
  solution: number;
  prefilledValue: string;
  rowIndex: number;
  colIndex: number;
}

export const SudokuCell = (props: ISudokuCellProps) => {
  const [solutionIsVisible, setSolutionIsVisble] = useState<boolean>(false);

  const switchSolutionVisibility = () => {
    setSolutionIsVisble((oldVisibility: boolean) => !oldVisibility);
  };

  const borderY = useMemo(() => {
    if (props.rowIndex % 3 === 0) {
      return " border-t-[6px]";
    } else {
      return " border-t-2";
    }
  }, [props.rowIndex]);

  const borderX = useMemo(() => {
    if (props.colIndex > 0 && props.colIndex % 3 === 0) {
      return " border-l-[6px]";
    } else {
      return " border-l-2";
    }
  }, [props.colIndex]);

  if (props.prefilledValue !== "") {
    let baseClass =
      "bg-beige align-middle text-center p-2 border-black border-solid font-bold text-2xl";
    baseClass += borderY;
    baseClass += borderX;
    return <td className={baseClass}>{props.solution}</td>;
  } else if (solutionIsVisible) {
    let baseClass =
      "bg-white align-middle text-center p-2 border-black border-solid font-bold text-2xl";
    baseClass += borderY;
    baseClass += borderX;
    return (
      <td onClick={switchSolutionVisibility} className={baseClass}>
        {props.solution}
      </td>
    );
  } else {
    let baseClass =
      "bg-blue align-middle text-center p-2 border-black border-solid font-bold text-2xl";
    baseClass += borderY;
    baseClass += borderX;
    return (
      <td onClick={switchSolutionVisibility} className={baseClass}>
        <span className="invisible">0</span>
      </td>
    );
  }
};
