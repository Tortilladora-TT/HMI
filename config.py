import logging

def configurar_logs(archivo_log=None, nivel=logging.INFO, reiniciar=True):
    """
    Configura el sistema de logging.
    
    :param archivo_log: Ruta del archivo de log. Si es None, solo se mostrarán logs en consola.
    :param nivel: Nivel de detalle del logging. Por defecto es INFO.
    :param reiniciar: Si True, sobrescribe el archivo de log al iniciar la aplicación.
    """
    formato = "%(asctime)s - [%(levelname)s] - (%(module)s.%(funcName)s) - %(message)s"
    handlers = [logging.StreamHandler()]  # Logs en consola

    # Añadir FileHandler si se especifica un archivo de log
    if archivo_log:
        modo = 'w' if reiniciar else 'a'  # 'w' para reiniciar, 'a' para anexar
        handlers.append(logging.FileHandler(archivo_log, mode=modo))

    logging.basicConfig(level=nivel, format=formato, handlers=handlers)


def cargar_estilos(app):
    """
    Carga los estilos de la aplicación

    :param app: Instancia de QApplication
    """
    try:
        with open("resources/styles.qss", "r") as archivo:
            app.setStyleSheet(archivo.read())
            logging.info("Estilos cargados correctamente")
    except FileNotFoundError:
        logging.error("El archivo de estilos no se encuentra.")
    except Exception as e:
        logging.error(f"Error al cargar estilos: {e}")
