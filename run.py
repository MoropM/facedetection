from facer import create_app

"""
    Indicamos que la aplicacion se ejecutara directamente
    por el nombre del archivo, en este caso run.py
"""
app = create_app()
if __name__ == '__main__':
    # app.run()
    app.run(host='0.0.0.0', port=4521) # Cualquier ip y un puerto en específico