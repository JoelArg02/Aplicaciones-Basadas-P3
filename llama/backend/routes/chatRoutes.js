import express from 'express';
import chatController from '../controllers/chatController.js';

const router = express.Router();

router.post('/chat/:userId', chatController.chat);

export default router;
