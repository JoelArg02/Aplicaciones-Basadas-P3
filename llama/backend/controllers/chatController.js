import ollama from 'ollama';
import faissIndexModel from '../models/faissIndexModel.js';
import memoryService from '../services/memoryService.js';

const chat = async (req, res) => {
    const userId = req.params.userId;
    
    // Obtener el historial de chat del usuario
    const userMemory = memoryService.getMemory(userId);
    const { pregunta } = req.body;

    // Buscar la respuesta más similar utilizando FAISS
    const respuesta_similar = faissIndexModel.buscarRespuesta(pregunta);

    // Construir el historial de mensajes para el modelo Ollama
    const messages = [
        ...userMemory.map(memory => ({ role: 'user', content: memory.pregunta })),
        { role: 'user', content: `${pregunta} ${respuesta_similar}` }
    ];

    // Utilizar Ollama para obtener una respuesta del modelo de lenguaje
    const response = await ollama.chat({
        model: 'llama3.1',
        messages: messages,
    });

    // Actualizar la memoria del usuario con la nueva interacción
    memoryService.updateMemory(userId, pregunta, response.message.content);

    // Enviar la respuesta al cliente
    res.json({ respuesta: response.message.content });
};

export default { chat };
