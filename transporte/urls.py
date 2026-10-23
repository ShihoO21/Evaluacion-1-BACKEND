from django.urls import path, include
from rest_framework import routers
from transporte import views

enrutador = routers.DefaultRouter()

enrutador.register(r'usuarios', views.UsuarioViewSet)
enrutador.register(r'conductores', views.ConductorViewSet)
enrutador.register(r'vehiculos', views.VehiculoViewSet)
enrutador.register(r'rutas', views.RutaViewSet)
enrutador.register(r'viajes', views.ViajeViewSet)
enrutador.register(r'historial-viajes', views.HistorialEstadoViajeViewSet)
enrutador.register(r'incidencias', views.IncidenciaViewSet)

urlpatterns = [
    path('', include(enrutador.urls)),
]