from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .models import Evento, RegistroEvento
from .forms import EventoForm, RegistroEventoForm
from .services import usuarios_registrados_evento, eventos_este_mes, usuarios_mas_activos, eventos_organizados_por_usuario

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistroUsuarioForm
from django.contrib.auth import logout
from django.http import HttpResponseNotAllowed

class EventoListView(ListView):
    model = Evento
    template_name = 'eventos/evento_list.html'
    context_object_name = 'eventos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['eventos_este_mes'] = eventos_este_mes()
        return context

class EventoDetailView(DetailView):
    model = Evento
    template_name = 'eventos/evento_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener los registros para el evento
        context['usuarios_registrados'] = RegistroEvento.objects.filter(evento=self.object)

        # Comprobar si el usuario actual está registrado
        context['estoy_registrado'] = RegistroEvento.objects.filter(evento=self.object, usuario=self.request.user).exists()

        return context

class EventoCreateView(LoginRequiredMixin, CreateView):
    model = Evento
    form_class = EventoForm
    template_name = 'eventos/evento_form.html'
    success_url = reverse_lazy('evento_list')

    def form_valid(self, form):
        form.instance.organizador = self.request.user
        return super().form_valid(form)

class EventoUpdateView(LoginRequiredMixin, UpdateView):
    model = Evento
    form_class = EventoForm
    template_name = 'eventos/evento_form.html'
    success_url = reverse_lazy('evento_list')

class EventoDeleteView(LoginRequiredMixin, DeleteView):
    model = Evento
    template_name = 'eventos/evento_confirm_delete.html'
    success_url = reverse_lazy('evento_list')

@login_required
def registro_evento(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)
    if request.method == 'POST':
        form = RegistroEventoForm(request.POST)
        if form.is_valid():
            registro = form.save(commit=False)
            registro.evento = evento
            registro.usuario = request.user
            registro.save()
            return redirect('evento_detail', pk=evento.pk)
    else:
        form = RegistroEventoForm()
    return render(request, 'eventos/registro_evento_form.html', {'form': form, 'evento': evento})

@login_required
def perfil_usuario(request):
    eventos_organizados = eventos_organizados_por_usuario(request.user.id)
    return render(request, 'eventos/perfil_usuario.html', {
        'eventos_organizados': eventos_organizados
    })

def usuarios_activos(request):
    usuarios = usuarios_mas_activos()
    return render(request, 'eventos/usuarios_activos.html', {'usuarios': usuarios})

def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('evento_list')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'eventos/registro.html', {'form': form})




#Login y logout
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('evento_list')
    else:
        form = AuthenticationForm()
    return render(request, 'eventos/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('evento_list')

