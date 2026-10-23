from django.shortcuts import render
from rest_framework import viewsets
from . import models, serializers


def bienvenida(request):
    return render(request, 'bienvenida.html')


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = models.Usuario.objects.all()
    serializer_class = serializers.UsuarioSerializer


class ConductorViewSet(viewsets.ModelViewSet):
    queryset = models.Conductor.objects.all()
    serializer_class = serializers.ConductorSerializer


class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = models.Vehiculo.objects.all()
    serializer_class = serializers.VehiculoSerializer


class RutaViewSet(viewsets.ModelViewSet):
    queryset = models.Ruta.objects.all()
    serializer_class = serializers.RutaSerializer


class ViajeViewSet(viewsets.ModelViewSet):
    queryset = models.Viaje.objects.all()
    serializer_class = serializers.ViajeSerializer


class HistorialEstadoViajeViewSet(viewsets.ModelViewSet):
    queryset = models.HistorialEstadoViaje.objects.all()
    serializer_class = serializers.HistorialEstadoViajeSerializer


class IncidenciaViewSet(viewsets.ModelViewSet):
    queryset = models.Incidencia.objects.all()
    serializer_class = serializers.IncidenciaSerializer