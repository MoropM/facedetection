from flask import render_template, Response, jsonify, Blueprint #, current_app
import os
import cv2
import uuid
import base64
from pathlib import Path
# import logging

bp = Blueprint('v1', __name__, url_prefix='/v1')


BASE_DIR = os.path.dirname(__file__) # facer

# uriHaarcascades = 'facer/Haarcascades/haarcascade_frontalface_default.xml'
uriHaarcascades = str(BASE_DIR + "/Haarcascades/haarcascade_frontalface_default.xml")
# path = 'facer/static'
path = str(BASE_DIR + "/static")
pathFile = path + '/media/'

# Inicializar el detector de caras
detector = cv2.CascadeClassifier(uriHaarcascades)


# Configurar logging
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')


# Creamos el directorio en caso de no existir
def createDir():
    try:
        if not os.path.exists(pathFile):
            os.makedirs(pathFile)

    except Exception as e:
        print(f"Error creando directorio: {e}")
        # current_app.logger.error(f"Error creando directorio: {e}")

# Obtenemos los frames del video (Camara)
def capture_by_frames():
    global camera
    global faces

    try:
        camera = cv2.VideoCapture(0)
        while True:
            ret, frame = camera.read()  # Leemos la cámara

            if not ret:
                break

            faces = detector.detectMultiScale(frame, 1.3, 6)  # Detectamos caras

            # for (x, y, w, h) in faces:
            #     cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Dibujamos rectángulo sobre las caras
            for (x, y, w, h) in faces: # Dibujamos un óvalo
                center = (x + w // 2, y + h // 2)
                axes = (w // 2, h // 2)
                cv2.ellipse(frame, center, axes, 0, 0, 360, (0, 255, 0), 2)

            _, jpeg = cv2.imencode('.jpg', frame)
            frame_bytes = jpeg.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

        camera.release()
    except Exception as e:
        print(f"Error en capture_by_frames: {e}")
        # current_app.logger.error(f"Error en capture_by_frames: {e}")

# Almacenamos y retornamos la url de la foto capturada
def guardar_foto():
    global camera
    global faces

    photoName = ''
    bytesFrame = ''
    statusCapture = False

    try:
        if len(faces) > 0:
            photoName = str(uuid.uuid4()) + '.jpg'
            ok, image = camera.read()
            # statusCapture = ok
            statusCapture = True
            if ok:
                (x, y, w, h) = faces[0]

                margin = 100
                y1 = max(0, y - margin)
                y2 = min(image.shape[0], y + h + margin)
                x1 = max(0, x - margin)
                x2 = min(image.shape[1], x + w + margin)
                rostro = image[y1:y2, x1:x2]

                resizeImg = cv2.resize(rostro, (450, 450), interpolation=cv2.INTER_CUBIC)
                # cv2.imwrite(str(pathFile / photoName), resizeImg)
                cv2.imwrite(pathFile + photoName, resizeImg)

                if photoName != '':
                    _, buffer = cv2.imencode('.jpg', resizeImg)
                    bytesFrame = base64.b64encode(buffer).decode('utf-8')

        return jsonify(
            {
                'message': "Capturando imagen",
                'status': statusCapture,
                'description': '',
                # 'path': pathFile,
                'path': str(pathFile),
                'photoName': photoName,
                'bytesFrame': bytesFrame,
            }
        )

    except Exception as e:
        print(f"Error en guardar_foto: {e}")
        statusCapture = False
        # current_app.logger.error(f"Error en guardar_foto: {e}")
        return jsonify(
        {
            'message': "Error al capturar la imagen",
            'status': statusCapture,
            'description': '',
            # 'path': pathFile,
            'path': str(pathFile),
            'photoName': photoName,
            'bytesFrame': bytesFrame,
        }
    )


# Iniciamos el proceso
@bp.route('/start', methods=['POST'])
def index():
    try:
        createDir()
        # capture_by_frames()
        return jsonify(
            {
                'status': True,
                'message': 'Inicializado',
                'description_path': '',
            }
        )
    except Exception as e:
        print(f"Error en index: {e}")
        # current_app.logger.error(f"Error en index: {e}")
        return jsonify(
            {
                'status': False,
                'message': 'Error al inicializar',
                'description': e,
                'description_path': '',
            }
        ), 500

# Retornamos el video
@bp.route('/video_capture')
def video_capture():
    try:
        return Response(capture_by_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception as e:
        print(f"Error en video_capture: {e}")
        # current_app.logger.error(f"Error en video_capture: {e}")
        return jsonify(
            {
                'status': False,
                'message': 'Error al capturar video',
                'description': e,
                'description_path': '',
            }
        ), 500

# Tomamos la foto
@bp.route('/take-photos', methods=['POST'])
def takePhotos():
    try:
        return guardar_foto()
    except Exception as e:
        print(f"Error en takePhotos: {e}")
        # current_app.logger.error(f"Error en takePhotos: {e}")
        return jsonify(
            {
                'status': False,
                'message': 'Error al tomar la foto',
                'description': e,
                'description_path': '',
            }
        ), 500

# Detenemos el video y captura de imagen
@bp.route('/stop')
def stop_capture():
    global camera
    try:
        if camera.isOpened():
            camera.release()
        return jsonify(
            {
                'message': "Proceso detenido",
                'status': True,
                'path': '',
                'photoName': '',
            }
        )
    except Exception as e:
        print(f"Error en stop_capture: {e}")
        # current_app.logger.error(f"Error en stop_capture: {e}")
        return jsonify(
            {
                'status': False,
                'message': 'Error al detener la captura',
                'description': e,
                'description_path': '',
            }
        ), 500

