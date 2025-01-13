from PyQt5.QtWidgets import QApplication, QStackedWidget
from PyQt5.QtGui import QGuiApplication
from pantallas.pantalla_principal import PantallaPrincipal
from pantallas.pantalla_diagnostico import PantallaDiagnostico
from pantallas.pantalla_automatico import PantallaAutomatico
from pantallas.pantalla_masa_disponible import PantallaMasaDisponible
from pantallas.pantalla_tortillas_deseadas import PantallaTortillasDeseadas
from pantallas.pantalla_operacion import PantallaOperacion
from config import cargar_estilos, configurar_logs
import logging

def obtener_resolucion():
    """
    Obtiene la resolución de la pantalla principal.
    """
    screen = QGuiApplication.primaryScreen()
    size = screen.size()
    return size.width(), size.height()

class MainApp(QStackedWidget):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height

        # Inicializar pantallas y pasar resolución
        self.pantalla_principal = PantallaPrincipal(self, width, height)
        self.pantalla_diagnostico = PantallaDiagnostico(self, width, height)
        self.pantalla_automatico = PantallaAutomatico(self, width, height)
        self.pantalla_masa_disponible = PantallaMasaDisponible(self, width, height)
        self.pantalla_tortillas_deseadas = PantallaTortillasDeseadas(self, width, height)
        self.pantalla_operacion = PantallaOperacion(self, width, height)

        # Agregar pantallas al stack
        self.addWidget(self.pantalla_principal)
        self.addWidget(self.pantalla_diagnostico)
        self.addWidget(self.pantalla_automatico)
        self.addWidget(self.pantalla_masa_disponible)
        self.addWidget(self.pantalla_tortillas_deseadas)
        self.addWidget(self.pantalla_operacion)

        # Configurar márgenes y ventana principal
        self.setContentsMargins(
            int(self.width * 0.02),  # Márgenes proporcionales a la resolución
            int(self.height * 0.02),
            int(self.width * 0.02),
            int(self.height * 0.02)
        )
        self.setWindowTitle("HMI - Selección de Modos")
        self.showFullScreen()  # Mostrar en pantalla completa

    def keyPressEvent(self, event):
        """
        Maneja las teclas globales.
        """
        from PyQt5.QtCore import Qt
        if event.key() == Qt.Key_Escape:
            logging.info("Aplicación cerrada por el usuario.")
            self.close()

if __name__ == "__main__":
    import sys

    # Configurar logs
    configurar_logs()
    logging.info("Iniciando la aplicación HMI")

    app = QApplication(sys.argv)

    # Obtener resolución de pantalla
    width, height = obtener_resolucion()
    logging.info(f"Resolución detectada: {width}x{height}")

    # Cargar estilos
    cargar_estilos(app)

    # Iniciar la aplicación principal
    main_app = MainApp(width, height)
    main_app.show()

    try:
        sys.exit(app.exec_())
    except Exception as e:
        logging.error(f"Error durante la ejecución de la aplicación: {e}")
