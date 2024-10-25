# Productos API

Este proyecto es una API para la gestión de productos, implementada con Flask. Utiliza JWT para la autenticación, MySQL como base de datos, y cuenta con pruebas unitarias utilizando Pytest. La documentación de la API está disponible en Swagger bajo el endpoint `/api`.

## Requisitos

Asegúrate de tener instaladas las siguientes herramientas:

- Python 3.11+
- Docker y Docker Compose (opcional)

## Configuración del Entorno

Es necesario crear un archivo `.env` en la raíz del proyecto con la siguiente configuración para la conexión a la base de datos y la clave secreta para JWT:

```
MYSQL_USER=user
MYSQL_PASSWORD=pass
MYSQL_DB=dbname
MYSQL_HOST=localhost
MYSQL_PORT=3306
JWT_SECRET=your_jwt_secret
DEBUG=True  # Opcional, para habilitar el modo de depuración
SWAGGER_URL=/api/docs  # Ruta para la documentación Swagger
```

## Instalación de Dependencias

Si deseas ejecutar el proyecto localmente, primero instala las dependencias necesarias. Puedes hacerlo con:

```bash
pip install -r requirements.txt
```

## Ejecución Local

Para ejecutar la API localmente, utiliza el siguiente comando:

```bash
# Para Mac o Linux
export FLASK_APP=run.py
export FLASK_ENV=development  # O 'production' según sea necesario
# Para Windows
set FLASK_APP=run.py
set FLASK_ENV=development

flask run
```

Accede a la API en [http://localhost:5000/api](http://localhost:5000/api) para la documentación de Swagger.

## Ejecución en Contenedor

Si prefieres ejecutar el proyecto en un contenedor Docker, asegúrate de tener configurado tu archivo `Dockerfile` y `docker-compose.yml`. Luego, ejecuta los siguientes comandos:

```bash
docker build -t products-api .
docker run -p 5000:5000 products-api
```

La API estará disponible en [http://localhost:5000/api](http://localhost:5000/api).

Considera que se crean dos usuarios de prueba para la configuración inicial del aplicativo. Estos usuarios son:

```javascript
[
    {'username': 'user1', 'password': 'password1'},
    {'username': 'user2', 'password': 'password2'}
]
```

## Caching

Se implementa un sistema de caching simple en memoria para almacenar temporalmente datos que son frecuentemente solicitados. Esto reduce la carga en la base de datos y mejora el rendimiento al evitar consultas repetidas.

## Pruebas Unitarias

Se realizaron un total de 9 pruebas unitarias en la API, todas ejecutadas con una base de datos SQLite en memoria. En esta base de datos se registra manualmente el usuario "test" con la contraseña "test" en cada uno de los casos de prueba para realizar el acceso correcto con autenticación, las pruebas incluidas son:

- **Autenticación/login**: Verifica el correcto funcionamiento del proceso de inicio de sesión.
- **Creación de producto**: Asegura que se puedan agregar nuevos productos a la base de datos.
- **Obtener listado de productos**: Comprueba que se pueda obtener un listado de todos los productos.
- **Obtener producto por ID**: Verifica la capacidad de recuperar un producto específico utilizando su ID.
- **Actualización de producto por ID**: Asegura que se pueda actualizar la información de un producto existente.
- **Eliminación de producto por ID**: Comprueba que se pueda eliminar un producto de la base de datos.
- **Paginado en listado de productos**: Verifica que el paginado funcione correctamente en el listado de productos.
- **Eliminación de producto inexistente**: Asegura que se maneje adecuadamente la eliminación de un producto que no existe.
- **Acceso inautorizado a servicio**: Comprueba que se restrinja el acceso a servicios sin la autorización adecuada.

Para realizar pruebas unitarias en la API, puedes usar Pytest. Si deseas ejecutar las pruebas en un entorno local, ejecuta:

```bash
pytest
```

Si estás ejecutando el proyecto en un contenedor, puedes cambiar el comando en el `Dockerfile` para incluir las pruebas, o ejecutar un contenedor separado solo para las pruebas.

## Notas Finales

Esta API está diseñada para ser flexible y escalable, pudiendo ser adaptada para trabajar con diferentes bases de datos SQL. La estructura del modelo de datos para productos es simple y bien definida, lo que facilita la implementación.
