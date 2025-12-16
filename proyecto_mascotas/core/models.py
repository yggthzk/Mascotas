from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Mascota(models.Model):
    TIPO_CHOICES = [('Perro', 'Perro'), ('Gato', 'Gato')]
    
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    descripcion = models.TextField()
    zona = models.CharField(max_length=100)
    fecha_reporte = models.DateTimeField(auto_now_add=True) #campos delformulario de creacion

    def __str__(self):
        return f"{self.nombre} ({self.tipo})"

@receiver(post_save, sender=Mascota)
def notificar_observadores(sender, instance, created, **kwargs):
    if created:
        print(f"--- [OBSERVER ALERT]: Se ha reportado una nueva mascota en {instance.zona}: {instance.nombre} ---")