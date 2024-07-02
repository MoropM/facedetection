from flask import render_template, Response, jsonify, Blueprint
from pathlib import Path
import os
import cv2
import uuid
import base64

bp = Blueprint('v1', __name__, url_prefix='/v1')


# BASE_DIR = Path(__file__).resolve().parent.parent

# path = BASE_DIR / "facer/static"
# pathFile = path / "media/"

# print(f"BASE_DIR: {BASE_DIR}")
# print(f"path: {path}")
# print(f"pathFile: {pathFile}")

detector = cv2.CascadeClassifier('facer/Haarcascades/haarcascade_frontalface_default.xml')
path = 'facer/static'
pathFile = path+'/media/'

#Creamos el directorio en caso de no existir
def createDir():
    #Crear carpeta en caso de que no exista
    if not os.path.exists(pathFile):
        os.makedirs(pathFile)

# Obtenemos los frames del video (Camara)
def capture_by_frames():
    global camera
    global faces
    camera = cv2.VideoCapture(0)
    while True:
        __, frame = camera.read() # Leemos la cámara

        faces = detector.detectMultiScale(frame, 1.3, 6) # Dibujamos un rectangulo sobre el frame detectado
        # auxFaces = faces

        for(x, y, w, h) in faces:
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)

        __, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Almacenamos y retornamos la url de la foto capturada
def guardar_foto():
    photoName = ''
    bytesFrame = ''
    statusCapture = False

    # Almacenamos la imagen solo si se detecto la cara
    if( len(faces) > 0 ):
        # Guaradamos la imagen en un archivo
        photoName = str(uuid.uuid4())+'.jpg'
        ok, image = camera.read()
        statusCapture = ok
        if ok:
            """
            """
            # ? Código actualizado

            (x, y, w, h) = faces[0]  # Tomamos la primera cara detectada
            # rostro = image[y:y + h, x:x + w]

            # Asegurarnos de que las coordenadas del recorte están dentro de los límites de la imagen
            # y1, y2 = max(0, y), min(y + h, image.shape[0])
            # x1, x2 = max(0, x), min(x + w, image.shape[1])
            # rostro = image[y1:y2, x1:x2]

            # Añadimos un margen de 50 píxeles alrededor del rostro
            # margin = 150
            margin = 100
            y1 = max(0, y - margin)
            y2 = min(image.shape[0], y + h + margin)
            x1 = max(0, x - margin)
            x2 = min(image.shape[1], x + w + margin)
            rostro = image[y1:y2, x1:x2]

            resizeImg = cv2.resize(rostro, (450, 450), interpolation=cv2.INTER_CUBIC)
            # Define la ruta completa al archivo de imagen a guardar
            """
                # Guarda la imagen usando la ruta completa
                # image_path = pathFile / photoName
                # cv2.imwrite(str(image_path), resizeImg)
            """
            cv2.imwrite(pathFile + photoName, resizeImg)
            # Si necesitas la imagen en formato base64:
            # __, buffer = cv2.imencode('.jpg', resizeImg)
            # bytesFrame = base64.b64encode(buffer).decode('utf-8')

            if photoName != '':
                __, buffer = cv2.imencode('.jpg', resizeImg)
                bytesFrame = base64.b64encode(buffer).decode('utf-8')

            """
                # ? Código anterior

                resizeImg = ''

                # for (x, y, w, h) in faces:
                #     xx = x + 150
                #     yy = y + 150
                #     ww = w + 150
                #     hh = h + 150
                #     rostro = image[y:yy+hh, x:xx+ww]
                #     resizeImg = cv2.resize(rostro, (450,450), interpolation=cv2.INTER_CUBIC) # Obtenemos el rostro de 150x150px
                cv2.imwrite(pathFile + photoName, image)
                # bytesFrame = base64.b64encode(b'texto a codificar')
                # bytesFrame = base64.encodestring(image)
            """

        # if photoName != '':
        #     __, buffer = cv2.imencode('.jpg', image)
        #     frame = buffer.tobytes()

    return jsonify(
        {
            'message': "Capturando imagen",
            'status': statusCapture,
            'path': pathFile,
            'photoName': photoName,
            'bytesFrame': bytesFrame,
        }
    )


# Iniciamos el preceso
@bp.route('/start', methods=['POST'])
def index():
    createDir()
    capture_by_frames()
    return jsonify(
        {
            'status': True,
            'message': 'Inicializado',
        }
    )
    # return render_template('index.html')


# Retornamos el video
@bp.route('/video_capture')
def video_capture():
    return Response(capture_by_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Tomamos la foto
@bp.route('/take-photos',methods=['POST'])
def takePhotos():
    # if camera.isOpened():
    #     camera.release()
    return guardar_foto()
    # return render_template('index.html')
    # return render_template('stop.html')

# Detenemos el video y captura de imagen
@bp.route('/stop')
def stop_capture():
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