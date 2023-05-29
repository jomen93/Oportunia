# Sistema de Recomendación de Empleo - Oportunia

Este proyecto utiliza el modelo GPT-3 de OpenAI para generar recomendaciones de trabajo personalizadas basándose en los detalles proporcionados por el usuario, como los años de experiencia, las habilidades y las aspiraciones salariales. 

## Configuración y ejecución

Para configurar y ejecutar el proyecto, sigue los pasos detallados a continuación:

### Instalación

1. Clona este repositorio en tu máquina local usando `https://github.com/jomen93/Oportunia.git`
2. Navega a la carpeta del proyecto: `cd Oportunia`
3. Instala las dependencias necesarias con: `pip install -r requirements.txt`

### Ejecución

1. Ejecuta el script `main.py` para generar las recomendaciones. Esto creará un archivo CSV en el directorio de datos con las recomendaciones para cada usuario.
2. Inicia el servidor FastAPI con: `uvicorn main:app --reload`
   Esto iniciará el servidor en `http://127.0.0.1:8000`

## Uso de la API

Para obtener las recomendaciones de empleo para un usuario específico, realiza una petición GET a la ruta `/recommendations/{user_id}`, donde `{user_id}` es el ID del usuario para el que deseas obtener las recomendaciones.

Por ejemplo, para obtener las recomendaciones para el usuario con ID 157, puedes hacer una petición a `http://127.0.0.1:8000/recommendations/157`

Puedes hacer esto en tu navegador o usando una herramienta como curl:

```bash
curl http://127.0.0.1:8000/recommendations/157
```

Esto devolverá una lista con las recomendaciones de empleo para el usuario solicitado, incluyendo los nombres de las vacantes y el puntaje de coincidencia.

