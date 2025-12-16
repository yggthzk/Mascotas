import google.generativeai as genai

API_KEY = "AIzaSyBfDZ63niATgaXItcilwqqXt0q3BFBLd-4" 

try:
    genai.configure(api_key=API_KEY)
    print("--- BUSCANDO MODELOS DISPONIBLES ---")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"Modelo encontrado: {m.name}")
except Exception as e:
    print(f"Error: {e}")