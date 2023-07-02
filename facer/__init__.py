from flask import Flask, render_template

def create_app():
    app = Flask(__name__)

    #Configuracion del proyecto
    app.config.from_mapping(
        DEBUG = False,
        SECRET = 'Aplicación d3 recon0cimI3nT= F4c!aLL 2=-3'
    )
    
    # registrar Blueprint
    from . import rekognition
    app.register_blueprint(rekognition.bp)

    @app.route('/')
    def index():
        return render_template('index.html')

    
    return app