
import logging

def configurar_logs():
    logging.basicConfig(
        filename="hmi_tortilla_machine.log",
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    logging.info("Sistema iniciado")

def cargar_estilos(app):
    try:
        with open("resources/styles.qss", "r") as archivo:
            app.setStyleSheet(archivo.read())
            logging.info("Estilos cargados correctamente")
    except FileNotFoundError:
        logging.error("El archivo de estilos no se encuentra.")
    except Exception as e:
        logging.error(f"Error al cargar estilos: {e}")