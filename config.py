def cargar_estilos(app):
    with open("resources/styles.qss", "r") as archivo:
        app.setStyleSheet(archivo.read())
