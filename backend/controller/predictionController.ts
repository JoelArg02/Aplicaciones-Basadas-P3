import { Request, Response } from "express";
import { PythonShell, Options } from "python-shell";

// Un objeto para almacenar los historiales de chat de los usuarios
const userSessions: { [key: string]: string[] } = {};

export const predictIncome = (req: Request, res: Response): void => {
  const { query, userId } = req.body;

  if (!userId) {
    res.status(400).json({ error: "userId es requerido" });
    return;
  }

  // Iniciar el historial del usuario si no existe
  if (!userSessions[userId]) {
    userSessions[userId] = [];
  }

  // Añadir la nueva consulta al historial del usuario
  userSessions[userId].push(query);

  const options: Options = {
    mode: "text",
    pythonOptions: ["-u"],
    scriptPath: "./models",
    args: [query],
    encoding: "utf8",
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

      // Añadir la respuesta al historial del usuario
      userSessions[userId].push(response.trim());

      res.json({ response: response.trim(), history: userSessions[userId] });
    }
  });
};
