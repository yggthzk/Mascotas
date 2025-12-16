import os
import django
import random


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto_mascotas.settings')
django.setup()

from core.models import Mascota

nombres = ["Luna", "Rocky", "Max", "Bella", "Simba", "Coco", "Lola", "Thor", "Nala", "Zeus", "Daisy", "Charlie", "Milo", "Buddy", "Toby", "Oreo", "Mia", "Jack", "Chloe", "Leo", "Nina", "Sombra", "Manchas", "Pelusa", "Duque", "Rex", "Bruno", "Kira", "Tobi", "Lucky", "Princesa", "Chester", "Pepe", "Fiona", "Dante", "Bimba", "Lulu", "Chispa", "Negro", "Blanca"]
colores = ["negro", "blanco", "cafe", "gris", "dorado", "manchado", "tricolor", "atigrado", "crema", "rojizo"]
adjetivos = ["pequeno", "grande", "amigable", "timido", "jugueton", "peludo", "de pelo corto", "viejo", "cachorro", "nervioso"]
detalles = ["tiene collar rojo", "cojea un poco", "responde al silbido", "tiene una cicatriz", "sin collar", "lleva panuelo azul", "tiene ojos de distinto color", "tiene la cola cortada", "orejas grandes", "muy ladrador"]
zonas = ["Plaza de Armas", "Parque Central", "Avenida Principal", "Sector Norte", "Barrio Sur", "Callejon Los Alamos", "Mercado Central", "Estacion de Tren", "Cerca del Rio", "Zona Industrial", "Villa Los Heroes", "Condominio Alto", "Callejon Oscuro", "Frente al Hospital", "Paradero 5"]

print("Iniciando generacion de 50 mascotas...")

for i in range(50):
    tipo_mascota = random.choice(['Perro', 'Gato'])
    nombre_elegido = random.choice(nombres)
    color_elegido = random.choice(colores)
    adj_elegido = random.choice(adjetivos)
    detalle_elegido = random.choice(detalles)
    zona_elegida = random.choice(zonas)

    descripcion_generada = f"{tipo_mascota} {color_elegido}, es bastante {adj_elegido}. Como seña particular {detalle_elegido}."

    Mascota.objects.create(
        nombre=nombre_elegido,
        tipo=tipo_mascota,
        descripcion=descripcion_generada,
        zona=zona_elegida
    )

print("Listo. Se han creado 50 mascotas exitosamente.")