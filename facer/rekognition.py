from flask import render_template, Response, jsonify, Blueprint
import os
import cv2
import uuid

bp = Blueprint('v1', __name__, url_prefix='/v1')

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

        # if photoName != '':
        #     __, buffer = cv2.imencode('.jpg', image)
        #     frame = buffer.tobytes()

    return jsonify(
        {
            'message': "Capturando imagen",
            'status': statusCapture,
            'path': pathFile,
            'photoName': photoName,
            # 'bytesFrame': bytesFrame,
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