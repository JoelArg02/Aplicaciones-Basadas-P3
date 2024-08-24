import faiss from 'faiss';
import vectorizerModel from './vectorizerModel.js';
import responseModel from './responseModel.js';

let index = null;

const loadIndex = () => {
    if (!index) {
        index = faiss.read_index('./faiss_index.index');
    }
    return index;
};

const buscarRespuesta = (pregunta) => {
    loadIndex();

    const vectorizer = vectorizerModel.loadVectorizer();
    const pregunta_vector = vectorizer.transform([pregunta]).toarray().astype('float32');

    const [D, I] = index.search(pregunta_vector, 1);

    const respuestas = responseModel.loadRespuestas();
    return respuestas[I[0][0]];
};

export default { buscarRespuesta };
