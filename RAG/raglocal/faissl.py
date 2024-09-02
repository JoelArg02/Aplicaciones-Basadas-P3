import sys
import json
import joblib
import faiss
import numpy as np
from flask import Flask, request, jsonify

app = Flask(__name__)

# Cargar el vectorizador y el índice FAISS
vectorizer = joblib.load('vectorizer.pkl')
index = faiss.read_index('faiss_index.index')

# Cargar respuestas
with open('respuestas.json', 'r', encoding='utf-8') as f:
    respuestas = json.load(f)

def buscar_respuesta(pregunta):
    # Convierte la pregunta en un vector
    pregunta_vector = vectorizer.transform([pregunta]).toarray().astype("float32")
    # Busca en el índice FAISS la pregunta más similar
    D, I = index.search(pregunta_vector, 1)
    # Retorna la respuesta correspondiente
    return respuestas[I[0][0]]

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    pregunta = data.get('pregunta')
    respuesta_similar = buscar_respuesta(pregunta)
    return jsonify({'respuesta': respuesta_similar})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
