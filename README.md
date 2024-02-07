# Documentación de la API

Información importante: la API actualiza automáticamente (usando python scheduler) cada minuto
al segundo 0 la información más reciente sobre el spread de cada mercado. Por lo tanto, la 
información puede tener hasta un minuto de desfase.

Este es un proyecto hecho con Python y Django. En /spreadAPI/management/updateSpreads.py
se puede encontrar la función update_spread(), la cual se encarga de guardar en la base de
datos la información del spread de cada mercado.

## Setup y Tests

Instalar docker y docker-compose en tu computador. Crear .env en la raiz del proyecto 
y poner las siguientes variables de entorno:

POSTGRES_DB=tarea_buda_db
POSTGRES_USER=tarea_buda_user
POSTGRES_PASSWORD=tarea_buda_password
DEBUG=True
SECRET_KEY=django-insecure-lg9%bb4wap7@ux@i8w(e2-&h=oxjxygt_5$z@az_!1ze*&vjt+
ALLOWED_HOSTS=localhost,127.0.0.1,[::1]

Posteriormente, iniciar docker y correr:

```
docker-compose build
docker-compose run web python manage.py makemigrations
docker-compose run web python manage.py migrate
docker-compose run web python manage.py updateSpreads
```

Para correr los tests:

```
docker-compose run web python manage.py test
```

Para levantar la aplicación:

```
docker-compose up
```

En caso de que haya algún problema:

```
docker-compose down
docker-compose up
```

## Obtener el spread de todos los mercados

```
localhost:8000/spreads
```

## Obtener el spread de un mercado

```
localhost:8000/spreads/{id}
```

En esta vista también se puede modificar el alert_spread en el json de abajo y pulsar el 
botón PATCH de la esquina inferior derecha para cambiar este parámetro
