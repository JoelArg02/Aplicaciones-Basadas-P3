from flask import Flask, request, jsonify, render_template
import requests
from langdetect import detect

app = Flask(__name__)

FAISS_URL = 'http://localhost:5001/search'
LLAMA_URL = 'http://localhost:5002/generate_llama'
COHERE_URL = 'http://localhost:5003/generate_cohere'
conversation_history = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/rag', methods=['POST'])
def rag():
    data = request.json
    pregunta = data.get('pregunta')

    # Paso 1: Detectar el idioma de la pregunta
    idioma = detect(pregunta)
    modelo = ''

    # Paso 2: Recuperar información relevante usando FAISS
    faiss_response = requests.post(FAISS_URL, json={'pregunta': pregunta})
    respuesta_similar = faiss_response.json().get('respuesta')

    # Paso 3: Refinar la respuesta usando el modelo adecuado
    if (idioma == 'es'):
        model_url = LLAMA_URL
        modelo = 'Llama 3.1'
    else:
        model_url = COHERE_URL
        modelo = 'Cohere'

    response = requests.post(model_url, json={
        'prompt': pregunta,
        'respuesta': respuesta_similar,
    })

    final_response = response.json().get('response')
    historial = response.json().get('historial')

    return jsonify({'respuesta': final_response, 'historial': historial, 'modelo':modelo })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
