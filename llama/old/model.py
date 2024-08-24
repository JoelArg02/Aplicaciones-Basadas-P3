from langchain_community.llms import Ollama
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import os
import joblib
import json
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import faiss
from langchain_community.llms import Ollama
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import unidecode

# Cargar el archivo JSON
file_path = 'data.json'
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Extraer preguntas y respuestas
preguntas = [entry['pregunta'] for entry in data]
respuestas = [entry['respuesta'] for entry in data]

# Vectorizar preguntas
vectorizer = TfidfVectorizer()
preguntas_vectores = vectorizer.fit_transform(preguntas).toarray()

# Crear el índice FAISS
dimension = preguntas_vectores.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(preguntas_vectores.astype('float32'))

# Guardar el modelo y el índice
joblib.dump(vectorizer, 'vectorizer.pkl')
faiss.write_index(index, 'faiss_index.index')

# Guardar respuestas
with open('respuestas.json', 'w', encoding='utf-8') as f:
    json.dump(respuestas, f)


import joblib

# Cargar el vectorizador
vectorizer = joblib.load('vectorizer.pkl')

# Obtener la versión de scikit-learn utilizada para entrenar el modelo
scikit_learn_version = vectorizer.__getstate__()['_sklearn_version']
print(f"Versión de scikit-learn usada para entrenar el modelo: {scikit_learn_version}")

# Guardar el modelo y el índice
joblib.dump(vectorizer, 'vectorizer.pkl')
faiss.write_index(index, 'faiss_index.index')

# Guardar respuestas
with open('respuestas.json', 'w', encoding='utf-8') as f:
    json.dump(respuestas, f)

# Configurar el modelo de lenguaje y el template de chat
llm = Ollama(model="llama3")
chat_history = []

prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """Eres un AI llamada Angela, respondes preguntas con respuestas simples,
            ademas debes contestar de vuelta preguntas acorde al contexto""",
        ),
        ("human", "{input}"),
    ]
)

chain = prompt_template | llm

def buscar_respuesta(pregunta):
    # Convierte la pregunta en un vector
    pregunta_vector = vectorizer.transform([pregunta]).toarray().astype("float32")
    # Busca en el índice FAISS la pregunta más similar
    D, I = index.search(pregunta_vector, 1)
    # Retorna la respuesta correspondiente
    return respuestas[I[0][0]]

def chat():
    while True:
        pregunta = input("You: ")
        if pregunta.lower() == "adios":
            return

        respuesta_similar = buscar_respuesta(pregunta)

        # Utilizar el modelo LLM para generar una respuesta final
        response = chain.invoke({"input": pregunta + " " + respuesta_similar, "chat_history": chat_history})
        chat_history.append(HumanMessage(content=pregunta))
        chat_history.append(AIMessage(content=response))
        print("-" * 50)
        print("AI: " + response)

chat()