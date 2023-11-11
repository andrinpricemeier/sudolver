import axios from "axios";

export class SudolverApi {
  async solve(imageBase64: string): Promise<any> {
    const result = await axios.post(
      "https://sudolver-api.fly.dev/sudoku/analysis",
      { image: imageBase64 },
      {
        headers: {
          "content-type": "application/json",
          "x-api-key": (window as any).ENV!.SUDOLVER_API_KEY,
        },
      }
    );
    return [result.data.solution, result.data.prefilled_table];
  }
}
