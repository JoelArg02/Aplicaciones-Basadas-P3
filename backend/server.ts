import cors from "cors";
import express, { Application } from "express";
import predictionRoutes from "./routes/predictionRoutes";

const app: Application = express();
const port: number = 3001;

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
