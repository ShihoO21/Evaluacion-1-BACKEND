import random
from datetime import timedelta
from decimal import Decimal

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from transporte.models import (Conductor, HistorialEstadoViaje, Incidencia,
                               Ruta, Usuario, Vehiculo, Viaje)

NOMBRES = ['Juan', 'Pedro', 'Diego', 'Matias', 'Felipe', 'Carlos', 'Luis', 'Jorge',
           'Andres', 'Cristian', 'Sebastian', 'Rodrigo', 'Pablo', 'Marcelo', 'Ricardo',
           'Maria', 'Camila', 'Valentina', 'Constanza', 'Javiera', 'Fernanda', 'Paula',
           'Carolina', 'Daniela', 'Francisca', 'Catalina', 'Ignacia', 'Sofia']
APELLIDOS = ['Gonzalez', 'Munoz', 'Rojas', 'Diaz', 'Perez', 'Soto', 'Contreras',
             'Silva', 'Martinez', 'Sepulveda', 'Morales', 'Rodriguez', 'Lopez',
             'Fuentes', 'Hernandez', 'Torres', 'Araya', 'Flores', 'Espinoza',
             'Valenzuela', 'Castillo', 'Tapia', 'Reyes', 'Gutierrez', 'Castro',
             'Pizarro', 'Alvarez', 'Vasquez', 'Sanchez', 'Fernandez']
CIUDADES = ['Arica', 'Iquique', 'Antofagasta', 'Calama', 'Copiapo', 'La Serena',
            'Valparaiso', 'Santiago', 'Rancagua', 'Talca', 'Chillan', 'Concepcion',
            'Temuco', 'Valdivia', 'Osorno', 'Puerto Montt', 'Punta Arenas',
            'Coyhaique', 'Los Angeles', 'Curico']
MARCAS = {
    'Mercedes-Benz': ['O500', 'Sprinter', 'Tourismo'],
    'Volvo': ['B8R', '9700'],
    'Scania': ['K360', 'K410'],
    'Marcopolo': ['Paradiso', 'Viaggio'],
    'Hyundai': ['County', 'H350'],
    'Iveco': ['Daily', 'Crossway'],
}
DESCRIPCIONES = {
    'MECANICA': ['Falla en el sistema de frenos', 'Recalentamiento del motor',
                 'Neumatico pinchado', 'Falla electrica en el tablero'],
    'ACCIDENTE': ['Colision leve en ruta', 'Choque por alcance sin lesionados'],
    'RETRASO': ['Demora por trafico', 'Retraso por condiciones climaticas',
                'Demora en control carretero'],
    'OTRO': ['Pasajero con malestar', 'Objeto olvidado a bordo',
             'Reclamo de pasajero'],
}


def calcular_dv(numero):
    suma, mult = 0, 2
    for digito in reversed(str(numero)):
        suma += int(digito) * mult
        mult = 2 if mult == 7 else mult + 1
    resto = 11 - (suma % 11)
    if resto == 11:
        return '0'
    if resto == 10:
        return 'K'
    return str(resto)


def valor_unico(generador, usados):
    while True:
        valor = generador()
        if valor not in usados:
            usados.add(valor)
            return valor


class Command(BaseCommand):
    help = 'Puebla la base de datos con datos de prueba para todas las tablas.'

    def add_arguments(self, parser):
        parser.add_argument('--cantidad', type=int, default=50,
                            help='Registros por tabla (viajes se crean el doble). Por defecto 50.')
        parser.add_argument('--limpiar', action='store_true',
                            help='Borra los datos existentes (menos superusuarios) antes de poblar.')

    def limpiar(self):
        Incidencia.objects.all().delete()
        HistorialEstadoViaje.objects.all().delete()
        Viaje.objects.all().delete()
        Conductor.objects.all().delete()
        Vehiculo.objects.all().delete()
        Ruta.objects.all().delete()
        Usuario.objects.filter(is_superuser=False).delete()
        self.stdout.write('Datos anteriores eliminados.')

    @transaction.atomic
    def handle(self, *args, **opciones):
        n = opciones['cantidad']
        if opciones['limpiar']:
            self.limpiar()

        ahora = timezone.now()
        clave = make_password('Clave12345')

        # ---------- Usuarios ----------
        usados = set(Usuario.objects.values_list('username', flat=True))
        roles = [r for r, _ in Usuario.Rol.choices]
        usuarios = []
        for i in range(n):
            nombre, apellido = random.choice(NOMBRES), random.choice(APELLIDOS)
            username = valor_unico(
                lambda: f"{nombre.lower()}.{apellido.lower()}{random.randint(1, 999)}", usados)
            usuarios.append(Usuario.objects.create(
                username=username, password=clave,
                first_name=nombre, last_name=apellido,
                email=f"{username}@transporte.cl",
                rol=roles[i % len(roles)],
                telefono=f"+569{random.randint(10000000, 99999999)}"))
        self.stdout.write(f'Usuarios creados: {len(usuarios)}')

        # ---------- Conductores ----------
        usados_rut = set(Conductor.objects.values_list('rut', flat=True))
        usados_lic = set(Conductor.objects.values_list('numero_licencia', flat=True))
        usuarios_conductor = [u for u in usuarios if u.rol == Usuario.Rol.CONDUCTOR]

        def generar_rut():
            numero = random.randint(8000000, 22000000)
            return f"{numero}-{calcular_dv(numero)}"

        conductores = []
        for _ in range(n):
            conductores.append(Conductor.objects.create(
                usuario=usuarios_conductor.pop(0) if usuarios_conductor else None,
                nombre=f"{random.choice(NOMBRES)} {random.choice(APELLIDOS)} {random.choice(APELLIDOS)}",
                rut=valor_unico(generar_rut, usados_rut),
                numero_licencia=valor_unico(
                    lambda: f"A{random.randint(1, 5)}-{random.randint(10000, 99999)}", usados_lic),
                vencimiento_licencia=ahora.date() + timedelta(days=random.randint(-90, 1500)),
                activo=random.random() > 0.1))
        self.stdout.write(f'Conductores creados: {len(conductores)}')

        # ---------- Vehiculos ----------
        usados_pat = set(Vehiculo.objects.values_list('patente', flat=True))
        letras = 'BCDFGHJKLPRSTVWXYZ'

        def generar_patente():
            return ''.join(random.choices(letras, k=4)) + f"{random.randint(10, 99)}"

        estados_vehiculo = [e for e, _ in Vehiculo.Estado.choices]
        vehiculos = []
        for _ in range(n):
            marca = random.choice(list(MARCAS))
            vehiculos.append(Vehiculo.objects.create(
                patente=valor_unico(generar_patente, usados_pat),
                marca=marca, modelo=random.choice(MARCAS[marca]),
                capacidad=random.choice([15, 20, 30, 40, 45, 50, 60]),
                estado=random.choice(estados_vehiculo),
                activo=random.random() > 0.1))
        self.stdout.write(f'Vehiculos creados: {len(vehiculos)}')

        # ---------- Rutas ----------
        pares = set()
        rutas = []
        while len(rutas) < n:
            origen, destino = random.sample(CIUDADES, 2)
            if (origen, destino) in pares:
                continue
            pares.add((origen, destino))
            km = Decimal(random.randint(50, 3000)) + Decimal(random.randint(0, 99)) / 100
            rutas.append(Ruta.objects.create(
                nombre=f"{origen}-{destino}", origen=origen, destino=destino,
                distancia_km=km,
                duracion_estimada_min=int(km / 70 * 60),
                publica=random.random() > 0.2,
                activa=random.random() > 0.1))
        self.stdout.write(f'Rutas creadas: {len(rutas)}')

        # ---------- Viajes e historial ----------
        creadores = [u for u in usuarios if u.rol != Usuario.Rol.CONDUCTOR] or [None]
        viajes = []
        total_historial = 0
        for _ in range(n * 2):
            ruta = random.choice(rutas)
            vehiculo = random.choice(vehiculos)
            salida = ahora + timedelta(days=random.randint(-90, 30),
                                       hours=random.randint(0, 23))
            if salida < ahora:
                estado = random.choice(['FINALIZADO', 'FINALIZADO', 'CANCELADO'])
            else:
                estado = random.choice(['PROGRAMADO', 'PROGRAMADO', 'CANCELADO'])
            llegada = (salida + timedelta(minutes=ruta.duracion_estimada_min)
                       if estado == 'FINALIZADO' else None)
            viaje = Viaje.objects.create(
                ruta=ruta, vehiculo=vehiculo, conductor=random.choice(conductores),
                creado_por=random.choice(creadores),
                fecha_salida=salida, fecha_llegada=llegada,
                pasajeros=random.randint(0, vehiculo.capacidad),
                estado=estado)
            viajes.append(viaje)

            if estado == 'FINALIZADO':
                cadena = [('NUEVO', 'PROGRAMADO'), ('PROGRAMADO', 'EN_CURSO'),
                          ('EN_CURSO', 'FINALIZADO')]
            elif estado == 'CANCELADO':
                cadena = [('NUEVO', 'PROGRAMADO'), ('PROGRAMADO', 'CANCELADO')]
            else:
                cadena = [('NUEVO', 'PROGRAMADO')]
            for anterior, nuevo in cadena:
                HistorialEstadoViaje.objects.create(
                    viaje=viaje, estado_anterior=anterior, estado_nuevo=nuevo,
                    usuario=random.choice(creadores),
                    observacion=f"Cambio de estado a {nuevo}")
                total_historial += 1
        self.stdout.write(f'Viajes creados: {len(viajes)}')
        self.stdout.write(f'Registros de historial creados: {total_historial}')

        # ---------- Incidencias ----------
        tipos = [t for t, _ in Incidencia.Tipo.choices]
        for _ in range(n):
            tipo = random.choice(tipos)
            Incidencia.objects.create(
                viaje=random.choice(viajes), tipo=tipo,
                descripcion=random.choice(DESCRIPCIONES[tipo]),
                resuelta=random.random() > 0.4,
                fecha=ahora - timedelta(days=random.randint(0, 60)))
        self.stdout.write(f'Incidencias creadas: {n}')

        self.stdout.write(self.style.SUCCESS('Base de datos poblada correctamente.'))