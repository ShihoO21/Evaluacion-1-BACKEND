# Gestión de Transporte - API REST

API REST desarrollada con **Django** y **Django REST Framework** para digitalizar
la gestión de rutas y viajes de una empresa de transporte. Centraliza conductores,
vehículos, rutas, viajes, historial de cambios de estado e incidencias, y expone
operaciones CRUD completas sobre cada entidad.

## Tecnologías

- Python 3.10 o superior
- Django
- Django REST Framework
- MySQL 8 (por ejemplo, mediante WAMP)
- PyMySQL
- python-decouple (variables de entorno)

## Modelo de datos

| Entidad | Descripción |
|---|---|
| Usuario | Usuario personalizado con rol (Administrador, Operador, Conductor) |
| Conductor | Datos del conductor y su licencia |
| Vehículo | Patente, marca, modelo, capacidad y estado |
| Ruta | Origen, destino, distancia y duración estimada; puede ser pública o privada |
| Viaje | Une ruta, vehículo y conductor, con fechas, pasajeros y estado |
| Historial de estado de viaje | Registro de cada cambio de estado, para auditoría |
| Incidencia | Eventos excepcionales asociados a un viaje |

## Instalación

1. Clonar el repositorio y entrar a la carpeta del proyecto.

2. Crear y activar el ambiente virtual:
   ```
   python -m venv GestionTransporte
   GestionTransporte\Scripts\activate
   ```

3. Instalar las dependencias:
   ```
   pip install -r requirements.txt
   ```

4. Crear la base de datos, el usuario y los permisos. Abrir phpMyAdmin con el
   usuario `root`, ir a la pestaña **SQL** y ejecutar el contenido de
   `sql/bdgestion.sql`.

5. Copiar `.env.example` como `.env` y completar los valores:
   ```
   SECRET_KEY='una_clave_secreta'
   DEBUG=True
   DB_NAME=transporte_db
   DB_USER=transporte_user
   DB_PASSWORD=la_contraseña_definida_en_el_script_sql
   DB_HOST=localhost
   DB_PORT=3306
   ```
   Para generar una SECRET_KEY:
   ```
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

6. Aplicar las migraciones:
   ```
   python manage.py migrate
   ```

7. Crear un superusuario:
   ```
   python manage.py createsuperuser
   ```

8. (Opcional) Cargar datos de prueba, con al menos 50 registros por tabla:
   ```
   python manage.py poblar_datos
   ```
   Opciones: `--cantidad 100` para generar más registros y `--limpiar` para
   borrar los datos anteriores antes de poblar (no elimina superusuarios).
   Los usuarios generados tienen la contraseña `Clave12345`.

9. Levantar el servidor:
   ```
   python manage.py runserver
   ```

## Uso

| Sección | URL |
|---|---|
| Portada | http://127.0.0.1:8000/ |
| API REST | http://127.0.0.1:8000/transporte/ |
| Panel de administración | http://127.0.0.1:8000/admin/ |

## Endpoints

Base: `http://127.0.0.1:8000/transporte/`

| Recurso | Ruta |
|---|---|
| Usuarios | `/usuarios/` |
| Conductores | `/conductores/` |
| Vehículos | `/vehiculos/` |
| Rutas | `/rutas/` |
| Viajes | `/viajes/` |
| Historial de viajes | `/historial-viajes/` |
| Incidencias | `/incidencias/` |

Cada recurso permite:

| Método | Acción | Ejemplo |
|---|---|---|
| GET | Listar | `/rutas/` |
| GET | Detalle | `/rutas/1/` |
| POST | Crear | `/rutas/` |
| PUT | Reemplazar | `/rutas/1/` |
| PATCH | Modificar parcialmente | `/rutas/1/` |
| DELETE | Eliminar | `/rutas/1/` |

### Ejemplo: crear una ruta (POST `/transporte/rutas/`)

```json
{
  "nombre": "Temuco-Santiago",
  "origen": "Temuco",
  "destino": "Santiago",
  "distancia_km": "680.50",
  "duracion_estimada_min": 480,
  "publica": true,
  "activa": true
}
```

### Formato de fechas

- Fecha: `30-05-2028`
- Fecha y hora: `01-11-2026 08:00:00`

### Orden recomendado para crear datos a mano

Los viajes dependen de otras tablas, por lo que conviene crear primero
rutas, vehículos y conductores, luego viajes, y por último incidencias e historial.

## Estructura del proyecto

```
.
├── motor_django/        # Configuración del proyecto (settings, urls)
├── transporte/          # Aplicación principal
│   ├── management/      # Comando poblar_datos
│   ├── migrations/      # Migraciones del modelo de datos
│   ├── static/          # Estilos CSS
│   ├── templates/       # Portada, 404 y plantillas de API y admin
│   ├── admin.py         # Registro de modelos en el admin
│   ├── models.py        # Modelo de datos
│   ├── serializers.py   # Serializers de DRF
│   ├── urls.py          # Rutas de la API (DefaultRouter)
│   └── views.py         # ModelViewSet
├── sql/
│   └── bdgestion.sql    # Base de datos, usuario y permisos
├── .env.example         # Plantilla de variables de entorno
├── manage.py
├── requirements.txt
└── README.md
```

## Variables de entorno

El archivo `.env` contiene la SECRET_KEY y las credenciales de la base de datos.
No se sube al repositorio. Para configurarlo se usa la plantilla `.env.example`.

## Autor

Sebastian Parra

Asignatura: Programación Backend
Docente: Erick Bailey Rebolledo
Evaluación N.° 2 - Desarrollo de API REST con Django REST Framework