import sys
import json
import joblib
import faiss
import numpy as np
from langchain_community.llms import Ollama

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

if __name__ == "__main__":
    pregunta = sys.argv[1]
    respuesta_similar = buscar_respuesta(pregunta)
    
    # Configurar el modelo de lenguaje Ollama
    llm = Ollama(model="llama3")
    
    prompt = f"""
    Eres un AI llamada ESPECITO, respondes preguntas con respuestas simples, 
    además debes contestar de vuelta preguntas acorde al contexto, sin embargo, si las preguntas salen fuera de la base de datos debes indicar que no tienes información sobre eso pero pronto podras resolverlo.
    {pregunta}
    {respuesta_similar}
    """
    
    # Ensure prompt is a list of strings
    prompts = [prompt]
    
    # Detailed logging
    print(f"Type of 'prompt': {type(prompt)}")  # Should be <class 'str'>
    print(f"Content of 'prompt': {prompt}")  # To verify the content of the string
    print(f"Type of 'prompts': {type(prompts)}")  # Should be <class 'list'>
    print(f"Content of 'prompts': {prompts}")  # To verify the content of the list
    print(f"Length of 'prompts': {len(prompts)}")  # Should be 1
    print(f"Type of first element in 'prompts': {type(prompts[0])}")  # Should be <class 'str'>

    # Generar la respuesta con Ollama, pasando el prompt como una lista de strings
    try:
        response = llm.generate(prompts)  # Ensure prompt is a list
    except ValueError as e:
        print(f"Caught ValueError: {e}")
        print(f"Type of 'prompts' inside except block: {type(prompts)}")
        print(f"Content of 'prompts' inside except block: {prompts}")

    # Inspeccionar la estructura del objeto response
    print(f"Type of 'response': {type(response)}")
    print(f"Content of 'response': {response}")

    # Ajustar el acceso a los datos según la estructura de response
    try:
        if hasattr(response, 'generations'):
            respuesta_texto = response.generations[0][0].text
        else:
            respuesta_texto = "Error: El objeto response no contiene el atributo 'generations'"
    except AttributeError as e:
        respuesta_texto = f"Error: {str(e)}"

    print(respuesta_texto)
