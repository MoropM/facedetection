# facedetection
Proyecto creado con [Flask](https://flask.palletsprojects.com/en/3.0.x/installation/) - Python.
Permite detectar la cara de una persona a través de la cámara de un dispositivo desde la WEB.


<!-- Asegúrese de que al menos una instancia de la aplicación se está ejecutando:
heroku ps:scale web=1
heroku logs --tail -->



- Verificar python:
```bash
    python --version
```

- Si aún no tienes virtualenv instalado, instálalo ejecutando:
```bash
    pip install virtualenv
```

- Crear entorno virtual:
```bash
    # python -m venv nombre_del_entorno
    
    py -3 -m venv .venv
```

- Activación de entorno virtual:
```bash
    # Windows OS
    .venv\Scripts\activate

    # macOS/Linux
    .venv/bin/activate
```
- Desactivación de entorno virtual:
```bash
    # Windows OS
    deactivate

    # macOS/Linux
    source bin/deactivate
```

- Creación de archivo de dependencias:
```bash
    python -m pip freeze > requirements.txt
```
- Instala las dependencias:
```bash
    pip install -r requirements.txt
```

- Verifica la instalación:
```bash
    pip list
```

- Instalar Flask:
```bash
    pip install Flask
```

- Ejecutar el programa:
```bash
    python run.py
```

