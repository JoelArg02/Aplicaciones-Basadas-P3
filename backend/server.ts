import express, { Application } from "express";
import bodyParser from "body-parser";
import cors from "cors";
import predictionRoutes from "./routes/predictionRoutes";

const app: Application = express();
const port: number = 3000;

app.use(
  cors({
    origin: "*",
    methods: "GET,HEAD,PUT,PATCH,POST,DELETE",
    optionsSuccessStatus: 204,
  })
);

app.use(express.json());

app.set("trust proxy", true);

app.use("/predict", predictionRoutes);

// Iniciar el servidor
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
