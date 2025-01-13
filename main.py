# main.py
from PyQt5.QtWidgets import QApplication, QStackedWidget, QMessageBox
from pantallas.pantalla_principal import PantallaPrincipal
from pantallas.pantalla_diagnostico import PantallaDiagnostico
from pantallas.pantalla_automatico import PantallaAutomatico
from pantallas.pantalla_masa_disponible import PantallaMasaDisponible
from pantallas.pantalla_tortillas_deseadas import PantallaTortillasDeseadas
from pantallas.pantalla_operacion import PantallaOperacion
from PyQt5.QtCore import Qt
from config import cargar_estilos, configurar_logs
import logging

class MainApp(QStackedWidget):
    def __init__(self):
        super().__init__()

        # Inicializar pantallas
        self.pantalla_masa_disponible = PantallaMasaDisponible(self)
        self.pantalla_tortillas_deseadas = PantallaTortillasDeseadas(self)
        self.pantalla_operacion = PantallaOperacion(self)
        self.pantalla_principal = PantallaPrincipal(self)
        self.pantalla_diagnostico = PantallaDiagnostico(self)
        self.pantalla_automatico = PantallaAutomatico(self)

        # Agregar pantallas al stack
        self.addWidget(self.pantalla_principal)
        self.addWidget(self.pantalla_diagnostico)
        self.addWidget(self.pantalla_automatico)
        self.addWidget(self.pantalla_masa_disponible)
        self.addWidget(self.pantalla_tortillas_deseadas)
        self.addWidget(self.pantalla_operacion)

        # Configuración de la ventana
        self.setWindowTitle("HMI - Selección de Modos")
        self.setStyleSheet("QStackedWidget { background-color: #f5f5f5; }")  # Fondo mejorado
        self.showFullScreen()  # Inicia en pantalla completa

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            logging.info("Aplicación cerrada por el usuario.")
            respuesta = QMessageBox.question(
                self,
                "Confirmar salida",
                "¿Está seguro de que desea salir?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if respuesta == QMessageBox.Yes:
                self.close()  # Cerrar la aplicación si presionas Esc

if __name__ == "__main__":
    import sys

    # Configurar logs
    configurar_logs()
    logging.info("Iniciando la aplicación HMI")

    app = QApplication(sys.argv)

    # Cargar estilos
    cargar_estilos(app)

    main_app = MainApp()
    main_app.show()
    
    try:
        sys.exit(app.exec_())
    except Exception as e:
        logging.error(f"Error durante la ejecución de la aplicación: {e}")