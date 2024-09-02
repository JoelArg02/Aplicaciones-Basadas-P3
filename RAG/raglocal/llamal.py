import openai
from flask import Flask, request, jsonify

app = Flask(__name__)

# Inicializar el cliente OpenAI con la API de LLaMA
client = openai.OpenAI(
    api_key="470e60048f3e40c9b6f7796f884c5772",
    base_url="https://api.aimlapi.com",
)

conversation_history = []

def respuesta_llama(respuesta):
    conversation = [
        {"role": "system", "content": "Eres un asistente virtual de la Universidad de las Fuerzas Armadas ESPE que solo mejora las respuestas:"}
    ]
    for entry in conversation_history:
        conversation.append({"role": entry['role'], "content": entry['message']})
    conversation.append({"role": "system", "content": f"Respuesta: {respuesta}"})
    conversation.append({"role": "assistant", "content": f"Respuesta mejorada: "})
    chat_completion = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        messages=conversation,
        #stop = ["\n"],
        temperature=0.7,
        max_tokens=100,
    )
    print(conversation)
    response = chat_completion.choices[0].message.content.strip()
    return response

@app.route('/generate_llama', methods=['POST'])
def generate_llama():
    data = request.json
    pregunta = data.get('prompt')
    respuestaf = data.get('respuesta')

    conversation_history.append({"role": "user", "message": pregunta})
    respuesta = respuesta_llama(respuestaf)
    conversation_history.append({"role": "assistant", "message": respuesta})
    
    return jsonify({'response': respuesta, 'historial': conversation_history})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002)
