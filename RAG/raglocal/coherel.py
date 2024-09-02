import cohere
from flask import Flask, request, jsonify

app = Flask(__name__)

# Inicializar el cliente con tu API Key
co = cohere.Client('vDCqToDbwy61ksSZuacEEi01EAaysDZi6aVAbsP9')

conversation_history = []

def generar_respuesta_cohere(pregunta, respuesta):

    
    # Construir el contexto de la conversación
    conversation = "Universidad de las Fuerzas Armadas ESPE:\n"
    for entry in conversation_history:
        conversation += f"{entry['role']}: {entry['message']}\n"
    conversation += f"Respuesta: {respuesta}\nRespuesta mejorada:"
    
    response = co.generate(
        prompt=conversation,
        max_tokens=100,
        stop_sequences=["\n"],
        temperature=0.7,
    )
    print(conversation)
    return response.generations[0].text.strip()

@app.route('/generate_cohere', methods=['POST'])
def generte_cohere():
    
    data = request.json
    pregunta = data.get('prompt')
    respuestaf = data.get('respuesta')

    conversation_history.append({"role": "User", "message": pregunta})
    respuesta = generar_respuesta_cohere(pregunta, respuestaf)
    conversation_history.append({"role": "AI", "message": respuesta})
    return jsonify({'response': respuesta, 'historial':conversation_history})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5003)
