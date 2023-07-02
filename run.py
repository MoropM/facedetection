from facer import create_app

"""
 Indicamos que la aplicacion se ejecutara directamente
 por el nombre del archivo, en este caso run.py
"""
app = create_app()
if __name__ == '__main__':
    app.run()