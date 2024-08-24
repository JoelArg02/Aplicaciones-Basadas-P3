import fs from 'fs';
import path from 'path';

let respuestas = null;

const loadRespuestas = () => {
    if (!respuestas) {
        const filePath = path.resolve('./data.json'); 
        const data = fs.readFileSync(filePath, 'utf-8');
        respuestas = JSON.parse(data);
    }
    return respuestas;
};

export default { loadRespuestas };
