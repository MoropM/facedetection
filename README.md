# facedetection
Proyecto creado con [Flask](https://flask.palletsprojects.com/en/3.0.x/installation/) - Python.
Permite detectar la cara de una persona a través de la cámara de un dispositivo desde la WEB.


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

# Windows OS
py -3 -m venv .venv

# macOS/Linux
python3 -m venv .venv
```

- Activación de entorno virtual:
```bash
# Windows OS
.venv\Scripts\activate

# macOS/Linux
. .venv/bin/activate
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

- Para restablecer el estado de autorización de la aplicación:
```bash
tccutil reset Camera
```


## Para mantener aplicación Flask ejecutándose
#### Herramientas para mantener tu aplicación en ejecución


**Método 1: `nohup`**


`nohup` (no hang up) es una forma sencilla de mantener tu aplicación en ejecución después de cerrar la sesión SSH.

1. Ingresa a tu entorno virtual.
2. Ejecuta tu archivo `run.py` con `nohup` y redirige la salida a un archivo para monitorear los registros.
```bash
nohup python run.py > output.log 2>&1 &
```
El símbolo `&` al final hace que el proceso se ejecute en segundo plano. La salida estándar y la salida de error se redirigen al archivo `output.log`.


**Método 2: `screen` o `tmux`**


- Usando `screen`:


1. Instala `screen` si no lo tienes ya instalado:
```bash
sudo yum install screen # Para Amazon Linux
sudo apt-get install screen # Para Ubuntu
```
2. Inicia una nueva sesión de `screen`:
```bash
screen -S mi_sesion
```
3. Ingresa a tu entorno virtual y ejecuta tu aplicación:
```bash
python run.py
```
4. Para desengancharte de la sesión sin detener el proceso, presiona **Ctrl+A** seguido de **D**.
5. Puedes volver a conectar a la sesión con:
```bash
screen -r mi_sesion
```


- Usando `tmux`:


1. Instala `tmux` si no lo tienes ya instalado:
```bash
sudo yum install tmux # Para Amazon Linux
sudo apt-get install tmux # Para Ubuntu
```
2. Inicia una nueva sesión de tmux:
```bash
tmux new -s mi_sesion
```
3. Ingresa a tu entorno virtual y ejecuta tu aplicación:
```bash
python run.py
```
4. Para desengancharte de la sesión sin detener el proceso, presiona **Ctrl+B** seguido de **D**.
5. Puedes volver a conectar a la sesión con:
```bash
tmux attach -t mi_sesion
```

**Método 3: `Supervisord`**


`supervisord` es un sistema de control de procesos que permite ejecutar aplicaciones y asegurarse de que se reinicien en caso de fallo.

1. Instala `supervisor`:
```bash
sudo yum install supervisor # Para Amazon Linux
sudo apt-get install supervisor # Para Ubuntu
```
2. Configura `supervisor` añadiendo una nueva configuración para tu aplicación. Abre el archivo de configuración de `supervisor` (por ejemplo, **/etc/supervisor/conf.d/myapp.conf**):
```bash
[program:mi_app]
command=/ruta/a/tu/entorno_virtual/bin/python /ruta/a/tu/run.py
directory=/ruta/a/tu/directorio_de_aplicacion
autostart=true
autorestart=true
stderr_logfile=/var/log/mi_app.err.log
stdout_logfile=/var/log/mi_app.out.log
```
3. Actualiza la configuración y reinicia `supervisor`:
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start mi_app
```
Estos métodos te permitirán mantener tu aplicación Flask en ejecución continua en tu instancia EC2 de AWS.


