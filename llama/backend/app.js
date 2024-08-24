import express from 'express';
import chatRoutes from './routes/chatRoutes.js';

const app = express();

app.use(express.json());
app.use('/api', chatRoutes);

const port = process.env.PORT || 3000;
app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});
