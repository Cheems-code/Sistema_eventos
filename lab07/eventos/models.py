from django.db import models
from django.contrib.auth.models import User

class Evento(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha = models.DateTimeField()
    organizador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='eventos_organizados')

    def __str__(self):
        return self.titulo

class RegistroEvento(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='registros')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='eventos_registrados')
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('evento', 'usuario')

    def __str__(self):
        return f"{self.usuario.username} - {self.evento.titulo}"