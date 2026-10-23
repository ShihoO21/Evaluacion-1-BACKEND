from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (Usuario, Conductor, Vehiculo, Ruta, Viaje,
                     HistorialEstadoViaje, Incidencia)

admin.site.register(Usuario, UserAdmin)
admin.site.register(Conductor)
admin.site.register(Vehiculo)
admin.site.register(Ruta)
admin.site.register(Viaje)
admin.site.register(HistorialEstadoViaje)
admin.site.register(Incidencia)