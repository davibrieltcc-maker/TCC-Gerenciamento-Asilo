from django.urls import path
from . import views

app_name = 'fisioterapia'

urlpatterns = [
    path('', views.lista, name='lista'),
    path('<int:pk>/', views.detalhe, name='detalhe'),
    path('nova/', views.novo, name='novo'),
    path('<int:pk>/editar/', views.editar, name='editar'),
    path('<int:pk>/autorizar/', views.autorizar, name='autorizar'),
    path('<int:pk>/rejeitar/', views.rejeitar, name='rejeitar'),
    path('<int:pk>/evolucao/', views.registrar_evolucao, name='evolucao'),
    path('<int:pk>/excluir/', views.excluir, name='excluir'),
]
