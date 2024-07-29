import { Request, Response } from "express";
import { PythonShell, Options } from "python-shell";

export const predictIncome = (req: Request, res: Response): void => {
  const { query } = req.body;

  const options: Options = {
    mode: "text",
    pythonOptions: ["-u"],
    scriptPath: "./models",
    args: [query],
  };

  const pyshell = new PythonShell("predictionModel.py", options);

  let response = "";

  pyshell.on("message", (message) => {
    console.log(message);
    response = message;
  });

  pyshell.end((err, code, signal) => {
    if (err) {
      console.error("Error:", err);
      res.status(500).send({ error: err.message });
    } else {
      console.log(
        "El script de Python terminó con el código:",
        code,
        "y la señal:",
        signal
      );
      res.json({ response: response.trim() });
    }
  });
};
