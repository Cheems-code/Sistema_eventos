# services.py
from django.db.models import Count
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Evento, RegistroEvento

def usuarios_registrados_evento(evento_id):
    return RegistroEvento.objects.filter(evento_id=evento_id).count()

def eventos_este_mes():
    now = timezone.now()
    return Evento.objects.filter(fecha__year=now.year, fecha__month=now.month).count()

def usuarios_mas_activos(limit=5):
    return User.objects.annotate(num_registros=Count('eventos_registrados')).order_by('-num_registros')[:limit]

def eventos_organizados_por_usuario(usuario_id):
    return Evento.objects.filter(organizador_id=usuario_id).count()