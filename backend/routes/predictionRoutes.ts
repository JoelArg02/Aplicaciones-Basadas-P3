import { Router } from 'express';
import { predictIncome } from '../controller/predictionController';

const router: Router = Router();

router.post('/', predictIncome);

export default router;
