import json
import faiss
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# Cargar los datos desde el archivo JSON
with open('data.json', 'r', encoding='utf-8') as f:
    faqs = json.load(f)

# Extraer preguntas y respuestas
preguntas = [faq['pregunta'] for faq in faqs]
respuestas = [faq['respuesta'] for faq in faqs]

# Vectorizar las preguntas usando TF-IDF
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(preguntas).toarray()

# Crear el índice FAISS
d = X.shape[1]
index = faiss.IndexFlatL2(d)
index.add(X)

def buscar_faq(query, k=1):
    vec_query = vectorizer.transform([query]).toarray()
    D, I = index.search(vec_query, k)
    return [respuestas[i] for i in I[0]]

class ActionBuscarFAQ(Action):

    def name(self) -> Text:
        return "action_buscar_faq"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        query = tracker.latest_message.get('text')
        respuesta = buscar_faq(query)
        dispatcher.utter_message(text=respuesta[0])
        return []
