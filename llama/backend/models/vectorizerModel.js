import fs from 'fs';

let vectorizer = null;

const loadVectorizer = () => {
    if (!vectorizer) {
        const data = fs.readFileSync('./vectorizer.json', 'utf8');
        vectorizer = JSON.parse(data);
    }
    return vectorizer;
};

export default { loadVectorizer };
