const memory = {};

const getMemory = (userId) => {
    if (!memory[userId]) {
        memory[userId] = [];
    }
    return memory[userId];
};

const updateMemory = (userId, pregunta, respuesta) => {
    if (!memory[userId]) {
        memory[userId] = [];
    }
    memory[userId].push({ pregunta, respuesta });
};

export default { getMemory, updateMemory };
