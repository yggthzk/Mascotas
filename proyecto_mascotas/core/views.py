from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Mascota
from .services import FabricaMascotas, BusquedaIADifusa, SistemaLog

@login_required
def lista_mascotas(request):
    mascotas = Mascota.objects.all().order_by('-fecha_reporte')
    return render(request, 'lista.html', {'mascotas': mascotas})

@login_required
def crear_mascota(request):
    if request.method == 'POST':
        try:
            datos = {
                'nombre': request.POST['nombre'],
                'tipo': request.POST['tipo'],
                'descripcion': request.POST['descripcion'],
                'zona': request.POST['zona']
            }
            FabricaMascotas.crear_mascota(Mascota, datos)
            
            SistemaLog().registrar_evento(request.user.username, f"Creo mascota {datos['nombre']}")
            
            messages.success(request, "Mascota reportada exitosamente.")
            return redirect('lista_mascotas')
            
        except ValueError as e:
            messages.error(request, str(e))
            
    return render(request, 'form.html')

@login_required
def buscar_mascota(request):
    query = request.GET.get('q')
    resultados = []
    if query:
        estrategia = BusquedaIADifusa()
        todos = Mascota.objects.all()
        resultados = estrategia.buscar(query, todos)
        
        SistemaLog().registrar_evento(request.user.username, f"Busqueda IA: {query}")
    
    return render(request, 'busqueda.html', {'resultados': resultados, 'query': query})

@login_required
def eliminar_mascota(request, id):
    mascota = get_object_or_404(Mascota, id=id)
    nombre = mascota.nombre
    mascota.delete()
    
    SistemaLog().registrar_evento(request.user.username, f"Elimino mascota {nombre}")
    return redirect('lista_mascotas')

@login_required
def editar_mascota(request, id):
    mascota = get_object_or_404(Mascota, id=id)
    if request.method == 'POST':
        mascota.nombre = request.POST['nombre']
        mascota.descripcion = request.POST['descripcion']
        mascota.zona = request.POST['zona']
        mascota.save()
        
        SistemaLog().registrar_evento(request.user.username, f"Edito mascota {mascota.nombre}")
        return redirect('lista_mascotas')
    return render(request, 'form.html', {'mascota': mascota})