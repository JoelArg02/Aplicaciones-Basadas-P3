import sys
import pickle
import faiss
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import cohere

# Inicializar Cohere
co = cohere.Client('OUxseEdjMfnqbmNkjQcNOcbLKkjFwHREtRJq72ZS')

# Cargar los datos desde el archivo pickle
with open('modelo_faiss.pkl', 'rb') as f:
    data = pickle.load(f)
    index = data['index']
    vectorizer = data['vectorizer']
    respuestas = data['respuestas']

# Historial de conversación
conversation_history = []
print("Modelo cargado correctamente")
def buscar_faq(query, k=1):
    vec_query = vectorizer.transform([query]).toarray()
    D, I = index.search(vec_query, k)
    return [respuestas[i] for i in I[0]]

def generar_respuesta_cohere(pregunta):
    respuesta_similar = buscar_faq(pregunta)
    
    if respuesta_similar and respuesta_similar[0]:
        return respuesta_similar[0]
    
    # Construir el contexto de la conversación
    conversation = "Universidad de las Fuerzas Armadas ESPE:\n"
    for entry in conversation_history:
        conversation += f"{entry['role']}: {entry['message']}\n"
    conversation += f"Usuario: {pregunta}\nRespuesta:"
    
    response = co.generate(
        prompt=conversation,
        max_tokens=100,
        stop_sequences=["\n"],
        temperature=0.7,
    )
    
    return response.generations[0].text.strip()

if __name__ == "__main__":
    query = sys.argv[1]
    conversation_history.append({"role": "Usuario", "message": query})
    respuesta = generar_respuesta_cohere(query)
    conversation_history.append({"role": "AI", "message": respuesta})
    print(conversation_history)

    print(respuesta)
