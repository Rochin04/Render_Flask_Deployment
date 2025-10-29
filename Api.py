import os
from flask import Flask, Response, request, jsonify
from flask_cors import CORS
# Se recomienda importar google.generativeai directamente
import google.generativeai as genai
from google.generativeai import types
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Inicializar la aplicación Flask
app = Flask(__name__)
CORS(app)

# --- CORRECCIÓN AQUÍ ---
# Configurar el cliente de GenAI usando la clave de la variable de entorno
try:
    # La forma recomendada y más común en versiones recientes
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
except KeyError:
    # Si la clave no está configurada, informa al usuario.
    print("Error: La variable de entorno GEMINI_API_KEY no está configurada.")
    exit()

def generate_stream(prompt):
    """
    Función generadora que llama a la API de Gemini y produce (yields)
    los chunks de la respuesta a medida que llegan.
    """
    # El modelo se inicializa de esta forma en las versiones más recientes
    model = genai.GenerativeModel("gemini-2.5-pro")#gemini-2.5-pro  gemini-2.5-flash
    # Llama a la API y va produciendo cada fragmento de la respuesta
    # La estructura para generar contenido también ha sido simplificada
    for chunk in model.generate_content(
        contents=prompt,
        stream=True,
    ):
        if chunk.text:
            yield chunk.text

@app.route('/generate', methods=['POST', 'OPTIONS'])
def handle_generation():
    """
    Endpoint de la API que recibe una pregunta (prompt) y devuelve
    la respuesta de Gemini como un stream.
    """
    # Verificar que la petición sea de tipo JSON
    if not request.is_json:
        return jsonify({"error": "La petición debe ser de tipo JSON"}), 400

    data = request.get_json()
    prompt = data.get('prompt')

    # Validar que el prompt exista
    if not prompt:
        return jsonify({"error": "El campo 'prompt' es requerido"}), 400

    # Retornar una respuesta en streaming
    return Response(generate_stream(prompt), mimetype='text/plain')

if __name__ == '__main__':
    # Ejecutar la aplicación en modo debug.
    app.run(debug=True, port=5000)
