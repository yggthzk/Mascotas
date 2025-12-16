import difflib
import logging
import google.generativeai as genai
from django.conf import settings
from abc import ABC, abstractmethod

logging.basicConfig(filename='acceso_seguro.log', level=logging.INFO, format='%(asctime)s - %(message)s')

class SistemaLog:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(SistemaLog, cls).__new__(cls)
        return cls._instancia

    def registrar_evento(self, usuario, accion):
        mensaje = f"[AUDITORIA] Usuario: {usuario} - Accion: {accion}"
        logging.info(mensaje)
        print(mensaje) 

class EstrategiaBusqueda(ABC):
    @abstractmethod
    def buscar(self, query, queryset):
        pass

class BusquedaIADifusa(EstrategiaBusqueda):
    def buscar(self, query, queryset):
        resultados = []
        SistemaLog().registrar_evento("SISTEMA", f"Ejecutando IA para: {query}")
        
        for mascota in queryset:
            secuencia = difflib.SequenceMatcher(None, mascota.descripcion.lower(), query.lower())
            ratio = secuencia.ratio()
            
            if ratio > 0.4 or query.lower() in mascota.descripcion.lower():
                resultados.append(mascota)
        return resultados

class FabricaMascotas:
    @staticmethod
    def crear_mascota(modelo_clase, datos):
        if len(datos['descripcion']) < 10:
            raise ValueError("La descripcion es muy corta. Minimo 10 caracteres.")
            
        nueva_mascota = modelo_clase(**datos)
        nueva_mascota.save()
        return nueva_mascota

class ChatbotIA:
 #mis credeniales de APi gemini
    API_KEY = "AIzaSyBfDZ63niATgaXItcilwqqXt0q3BFBLd-4"
    
    @staticmethod
    def obtener_contexto_db(mensaje_usuario):
        from .models import Mascota
        
        # Buscamos mascotas relevantes en la DB local para darle contexto a Gemini
        todas = Mascota.objects.all()
        coincidencias = []
        for m in todas:
            if m.tipo.lower() in mensaje_usuario.lower() or m.zona.lower() in mensaje_usuario.lower() or m.nombre.lower() in mensaje_usuario.lower():
                coincidencias.append(f"- {m.nombre} ({m.tipo}) en {m.zona}: {m.descripcion}")
        
        # Limitamos a 5 para no saturar
        return "\n".join(coincidencias[:5])

    @staticmethod
    def responder(mensaje_usuario):
        try:
            # 1. Configurar Gemini
            genai.configure(api_key=ChatbotIA.API_KEY)
            model = genai.GenerativeModel('gemini-pro')
            
            # 2. Obtener datos reales de la DB (RAG)
            contexto_datos = ChatbotIA.obtener_contexto_db(mensaje_usuario)
            
            # PROMPT PA QUE SE COMPORTE COMO EMPLEADO DE LA APP MASOCTAS BIENESTAR
            prompt_sistema = f"""
            Actua como el asistente virtual experto y empatico de la app 'Bienestar animal perros y gatos perdidos App'.
            Tu mision es ayudar a encontrar mascotas perdidas y promover la adopcion.
            
            REGLAS STRICTAS:
            1. Solo responde temas de mascotas, seguridad y la app. Si te preguntan otra cosa, niegate educadamente.
            2. Usa la informacion de CONTEXTO DE DATOS para responder si aplica.
            3. Respuestas cortas (maximo 2 parrafos).
            
            CONTEXTO DE DATOS (Mascotas reales en base de datos):
            {contexto_datos}
            
            PREGUNTA DEL USUARIO:
            {mensaje_usuario}
            """
            
            #Generar respuesta
            response = model.generate_content(prompt_sistema)
            return response.text
            
        except Exception as e:
            print(f"Error Gemini: {e}")
            # FALLBACK: Si falla Gemini (sin internet o sin clave), responde con logica basica
            return ChatbotIA.responder_fallback(mensaje_usuario)
