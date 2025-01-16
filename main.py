import threading
import RPi.GPIO as GPIO
import time
from PyQt5.QtWidgets import QApplication, QStackedWidget, QMessageBox, QDialog, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from pantallas.pantalla_principal import PantallaPrincipal
from pantallas.pantalla_diagnostico import PantallaDiagnostico
from pantallas.pantalla_automatico import PantallaAutomatico
from pantallas.pantalla_masa_disponible import PantallaMasaDisponible
from pantallas.pantalla_tortillas_deseadas import PantallaTortillasDeseadas
from pantallas.pantalla_operacion import PantallaOperacion
from config import configurar_logs, cargar_estilos
import logging


class MainApp(QStackedWidget):
    GPIO_PIN = 16  # Definir el pin GPIO para el Paro de Emergencia

    def __init__(self):
        super().__init__()

        # Configurar GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

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
        self.setStyleSheet("QStackedWidget { background-color: #f4f6ff; }")
        self.showFullScreen()

        # Iniciar el monitor del GPIO
        self.monitor_gpio = threading.Thread(target=self.monitor_paro_emergencia, daemon=True)
        self.monitor_gpio.start()

    def cambiar_pantalla(self, pantalla):
        """Cambia a una pantalla específica y registra el cambio."""
        try:
            self.setCurrentWidget(pantalla)
            logging.info(f"Cambiando a la pantalla: {pantalla.__class__.__name__}")
        except Exception as e:
            logging.error(f"Error al cambiar de pantalla: {e}")

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
                self.close()

    def activar_paro_emergencia(self):
        """Muestra un dialog para el paro de emergencia."""
        dialog = QDialog(self)
        dialog.setWindowTitle("PARO DE EMERGENCIA")
        dialog.setModal(True)
        dialog.setFixedSize(400, 200)

        # Layout del dialog
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        # Texto del mensaje
        label = QLabel("PARO DE EMERGENCIA ACTIVADO")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 18px; font-weight: bold; color: red;")
        layout.addWidget(label)

        dialog.setLayout(layout)
        dialog.exec_()  # Mostrar el dialog

    def monitor_paro_emergencia(self):
        """Monitoriza el estado del GPIO para activar el paro de emergencia."""
        while True:
            estado = GPIO.input(self.GPIO_PIN)
            if estado == GPIO.HIGH:  # Detectar señal alta
                logging.warning("Paro de emergencia detectado desde el GPIO.")
                self.activar_paro_emergencia()
            time.sleep(0.1)  # Evitar uso excesivo de CPU


if __name__ == "__main__":
    import sys

    # Configurar logs
    configurar_logs("hmi_tortilla_machine.log", nivel=logging.DEBUG, reiniciar=True)
    logging.info("Iniciando la aplicación HMI")

    # Configurar GPIO
    GPIO.setwarnings(False)

    app = QApplication(sys.argv)

    # Cargar estilos
    cargar_estilos(app)

    main_app = MainApp()
    main_app.show()

    try:
        sys.exit(app.exec_())
    except Exception as e:
        logging.error(f"Error durante la ejecución de la aplicación: {e}")
    finally:
        GPIO.cleanup()  # Asegurarse de limpiar los GPIO al salir
