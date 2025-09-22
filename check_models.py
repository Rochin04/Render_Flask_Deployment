import google.generativeai as genai
import os
from dotenv import load_dotenv
import google.api_core.exceptions

# Cargar las variables de entorno desde .env
load_dotenv()

try:
    # Configurar la API key
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise KeyError("La variable de entorno GEMINI_API_KEY no fue encontrada en el archivo .env")
    
    genai.configure(api_key=api_key)

    print("-" * 50)
    print("Buscando modelos disponibles para tu clave de API...")
    print("-" * 50)

    # Listar todos los modelos y verificar los que soportan 'generateContent'
    found_models = False
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ Modelo encontrado: {m.name}")
            found_models = True

    if not found_models:
        print("\n❌ No se encontraron modelos que soporten 'generateContent'.")
        print("Esto confirma que hay un problema con la configuración de tu proyecto en Google Cloud o tu clave de API.")
        print("Causas posibles: Restricciones geográficas, problemas con la cuenta de facturación, o un retraso muy largo en la activación de la API.")

except KeyError as e:
    print(f"Error de Configuración: {e}")
except google.api_core.exceptions.PermissionDenied as e:
    print(f"❌ Error de Permiso Denegado: {e}")
    print("Esto significa que la 'Generative Language API' no está habilitada correctamente o tu clave no tiene permisos.")
except Exception as e:
    print(f"❌ Ocurrió un error inesperado: {e}")