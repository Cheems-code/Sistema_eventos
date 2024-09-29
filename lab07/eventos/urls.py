from django.urls import path
from . import views

urlpatterns = [
    path('', views.EventoListView.as_view(), name='evento_list'),
    path('evento/<int:pk>/', views.EventoDetailView.as_view(), name='evento_detail'),
    path('evento/nuevo/', views.EventoCreateView.as_view(), name='evento_create'),
    path('evento/<int:pk>/editar/', views.EventoUpdateView.as_view(), name='evento_update'),
    path('evento/<int:pk>/eliminar/', views.EventoDeleteView.as_view(), name='evento_delete'),
    path('evento/<int:evento_id>/registro/', views.registro_evento, name='registro_evento'),
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    path('usuarios-activos/', views.usuarios_activos, name='usuarios_activos'),
    
    #inicio de sesion 
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro_usuario, name='registro'),
]