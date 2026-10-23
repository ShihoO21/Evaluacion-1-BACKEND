from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class Usuario(AbstractUser):
    class Rol(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrador'
        OPERADOR = 'OPERADOR', 'Operador'
        CONDUCTOR = 'CONDUCTOR', 'Conductor'

    rol = models.CharField(max_length=10, choices=Rol.choices, default=Rol.OPERADOR)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.username


class Conductor(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='conductor')
    nombre = models.CharField('Nombre', max_length=100)
    rut = models.CharField('RUT', max_length=12, unique=True)
    numero_licencia = models.CharField('N° licencia', max_length=20, unique=True)
    vencimiento_licencia = models.DateField('Vencimiento licencia')
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre


class Vehiculo(models.Model):
    class Estado(models.TextChoices):
        DISPONIBLE = 'DISPONIBLE', 'Disponible'
        EN_RUTA = 'EN_RUTA', 'En ruta'
        MANTENCION = 'MANTENCION', 'En mantención'

    patente = models.CharField(max_length=10, unique=True)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    capacidad = models.PositiveIntegerField('Capacidad de pasajeros')
    estado = models.CharField(max_length=12, choices=Estado.choices, default=Estado.DISPONIBLE)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.patente


class Ruta(models.Model):
    nombre = models.CharField(max_length=100)
    origen = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    distancia_km = models.DecimalField(max_digits=7, decimal_places=2)
    duracion_estimada_min = models.PositiveIntegerField('Duración estimada (min)')
    publica = models.BooleanField('Información pública', default=True)
    activa = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} ({self.origen} - {self.destino})"


class Viaje(models.Model):
    class Estado(models.TextChoices):
        PROGRAMADO = 'PROGRAMADO', 'Programado'
        EN_CURSO = 'EN_CURSO', 'En curso'
        FINALIZADO = 'FINALIZADO', 'Finalizado'
        CANCELADO = 'CANCELADO', 'Cancelado'

    ruta = models.ForeignKey(Ruta, on_delete=models.PROTECT, related_name='viajes')
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.PROTECT, related_name='viajes')
    conductor = models.ForeignKey(Conductor, on_delete=models.PROTECT, related_name='viajes')
    creado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='viajes_creados')
    fecha_salida = models.DateTimeField()
    fecha_llegada = models.DateTimeField(null=True, blank=True)
    pasajeros = models.PositiveIntegerField(default=0)
    estado = models.CharField(max_length=12, choices=Estado.choices, default=Estado.PROGRAMADO)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Viaje {self.pk} - {self.ruta.nombre}"


class HistorialEstadoViaje(models.Model):
    viaje = models.ForeignKey(Viaje, on_delete=models.CASCADE, related_name='historial')
    estado_anterior = models.CharField(max_length=12)
    estado_nuevo = models.CharField(max_length=12)
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='cambios_estado')
    observacion = models.TextField(blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.viaje_id}: {self.estado_anterior} -> {self.estado_nuevo}"


class Incidencia(models.Model):
    class Tipo(models.TextChoices):
        MECANICA = 'MECANICA', 'Falla mecánica'
        ACCIDENTE = 'ACCIDENTE', 'Accidente'
        RETRASO = 'RETRASO', 'Retraso'
        OTRO = 'OTRO', 'Otro'

    viaje = models.ForeignKey(Viaje, on_delete=models.CASCADE, related_name='incidencias')
    tipo = models.CharField(max_length=10, choices=Tipo.choices, default=Tipo.OTRO)
    descripcion = models.TextField()
    resuelta = models.BooleanField(default=False)
    fecha = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.tipo} - viaje {self.viaje_id}"