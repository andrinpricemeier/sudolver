import { useCallback, useRef, useState } from "react";
import type { ImageBase64 } from "~/services/ImageBase64";
import { SolvingState } from "~/services/SolvingState";
import { SudolverApi } from "../services/SudolverApi";
import { BottomBar } from "./BottomBar";
import { Camera } from "./Camera";
import { ErrorMessage } from "./ErrorMessage";
import { ProgressIndicator } from "./ProgressIndicator";
import { ReloadButton } from "./ReloadButton";
import type { PrefilledGrid, SudokuGrid } from "./SudokuSolution";
import { SudokuSolution } from "./SudokuSolution";
import { SudolverTitle } from "./SudolverTitle";
import { TakeSnapshotButton } from "./TakeSnapshotButton";
import { TopBar } from "./TopBar";
import { Workspace } from "./Workspace";

export const MainApp = () => {
  const [solvingState, setSolvingState] = useState<SolvingState>(
    SolvingState.TAKING_PICTURE
  );
  const [solution, setSolution] = useState<[SudokuGrid, PrefilledGrid]>([
    [],
    [],
  ]);
  const cameraRef = useRef();

  const snapshotTaken = useCallback(async (imageBase64: ImageBase64) => {
    console.log("Setting screenshot");
    setSolvingState((_) => SolvingState.IN_PROGRESS);
    const api = new SudolverApi();
    try {
      const solution = await api.solve(imageBase64.getImageBase64());
      console.log("Success.");
      console.log(solution);
      setSolvingState((_) => SolvingState.SUCCESS);
      setSolution((_: any) => solution);
    } catch (ex) {
      console.log("Failed.");
      console.error(ex);
      setSolvingState((_) => SolvingState.FAILED);
    }
  }, []);

  const onTakeSnapshotClick = useCallback(() => {
    if (!cameraRef || !cameraRef.current) {
      return;
    }
    (cameraRef.current as any).takePicture();
  }, []);

  const onReloadClick = useCallback(() => {
    console.log("Reloaded!");
    setSolvingState((_) => SolvingState.TAKING_PICTURE);
  }, []);

  const getWorkspaceItem = () => {
    console.log("Getting workspace item.");
    switch (solvingState) {
      case SolvingState.TAKING_PICTURE:
        return (
          <Camera key="camera" snapshotTaken={snapshotTaken} ref={cameraRef} />
        );
      case SolvingState.IN_PROGRESS:
        return <ProgressIndicator key="progress" />;
      case SolvingState.SUCCESS:
        return <SudokuSolution key="solution" solution={solution} />;
      case SolvingState.FAILED:
        return <ErrorMessage onClick={onReloadClick} key="error-message" />;
    }
  };

  return (
    <main className="flex flex-col h-screen">
      <TopBar>
        <SudolverTitle />
      </TopBar>
      <Workspace children={[getWorkspaceItem()]}></Workspace>
      <BottomBar>
        <TakeSnapshotButton key="take-snapshot" onClick={onTakeSnapshotClick} />
        <ReloadButton key="reload" onClick={onReloadClick} />
      </BottomBar>
    </main>
  );
};
