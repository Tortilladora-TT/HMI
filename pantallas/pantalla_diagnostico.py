from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt, QTimer
from utils.base_ui import BaseUI
from utils.serial_manager import SerialManager
import logging

class PantallaDiagnostico(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        # Instancias de SerialManager para diferentes módulos
        self.arduino_compresion = SerialManager(port='/dev/ttyUSB0', baudrate=9600)
        self.arduino_coccion = SerialManager(port='/dev/AMA0', baudrate=9600)
        self.dialog_active = False  # Indica si hay un diálogo activo
        self.init_ui()

    def init_ui(self):
        # Configuración del layout principal
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        # Título
        layout.addWidget(BaseUI.crear_encabezado("Modo Diagnóstico"))

        # Subtítulo
        layout.addWidget(BaseUI.crear_subtitulo("Selecciona la opción que le gustaría verificar.\nRecuerda: este modo es SIN MASA"))

        # Espaciador superior para separar el texto de los botones
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Botones principales
        botones_layout = QVBoxLayout()
        botones_layout.setAlignment(Qt.AlignCenter)
        botones_layout.setSpacing(15)

        # Botones añadidos al layout
        botones_layout.addWidget(BaseUI.crear_boton("DOSIFICACIÓN", self.dosificacion))
        botones_layout.addWidget(BaseUI.crear_boton("COMPRESIÓN Y CORTE", self.compresion_corte))
        botones_layout.addWidget(BaseUI.crear_boton("COCCIÓN", self.coccion))

        # Añadir layout de botones al layout principal
        layout.addLayout(botones_layout)

        # Espaciador inferior para el botón de regresar
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Botón para regresar
        layout.addWidget(BaseUI.crear_boton("↩️ Regresar", self.regresar), alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def dosificacion(self):
        logging.info("Iniciando diagnóstico del módulo de dosificación")
        dialog = BaseUI.crear_alerta(self, "Verificando Módulo de Dosificación", "Esperando datos del módulo...")
        QTimer.singleShot(5000, dialog.accept)  # Cerrar automáticamente después de 5 segundos
        logging.info("Módulo de dosificación validado correctamente")
        dialog.exec_()

    def compresion_corte(self):
        logging.info("Iniciando diagnóstico del módulo de compresión y corte")
        if not self.arduino_compresion.connection or not self.arduino_compresion.connection.is_open:
            self.arduino_compresion.connect()

        if not self.arduino_compresion.connection:
            dialog = BaseUI.crear_alerta(self, "Error", "No se pudo conectar al módulo de compresión y corte.")
            dialog.exec_()
            return

        self.dialog_active = True
        dialog = BaseUI.crear_alerta(self, "Verificando Módulo de Compresión y Corte", "Esperando respuesta del Arduino...")

        def read_response():
            if not self.dialog_active:
                self.arduino_compresion.disconnect()  # Cerrar conexión si se interrumpe
                return

            response = self.arduino_compresion.read_response()
            if response:
                if response == "RSwitches":
                    dialog.layout().itemAt(0).widget().setText("Switches: Correcto")
                elif response == "ESwitches":
                    dialog.layout().itemAt(0).widget().setText("Switches: Error")
                    QTimer.singleShot(2000, lambda: self.finalizar_dialogo(dialog, self.arduino_compresion))
                    return
                elif response == "RMotores":
                    dialog.layout().itemAt(0).widget().setText("Motores: Correcto")
                elif response == "EMotores":
                    dialog.layout().itemAt(0).widget().setText("Motores: Error")
                    QTimer.singleShot(2000, lambda: self.finalizar_dialogo(dialog, self.arduino_compresion))
                    return
                elif response == "RIR":
                    dialog.layout().itemAt(0).widget().setText("Sensor IR: Correcto")
                    QTimer.singleShot(2000, lambda: self.finalizar_dialogo(dialog, self.arduino_compresion))
                    return
                elif response == "EIR":
                    dialog.layout().itemAt(0).widget().setText("Sensor IR: Error")
                    QTimer.singleShot(2000, lambda: self.finalizar_dialogo(dialog, self.arduino_compresion))
                    return
                else:
                    dialog.layout().itemAt(0).widget().setText(f"Respuesta desconocida: {response}")

                # Continuar leyendo
                QTimer.singleShot(500, read_response)
            else:
                dialog.layout().itemAt(0).widget().setText("Sin respuesta del módulo.")
                QTimer.singleShot(2000, lambda: self.finalizar_dialogo(dialog, self.arduino_compresion))

        read_response()
        dialog.exec_()


    def coccion(self):
        logging.info("Iniciando diagnóstico del módulo de cocción")
        if not self.arduino_coccion.connection or not self.arduino_coccion.connection.is_open:
            self.arduino_coccion.connect()

        if not self.arduino_coccion.connection:
            dialog = BaseUI.crear_alerta(self, "Error", "No se pudo conectar al módulo de cocción.")
            dialog.exec_()
            return

        self.dialog_active = True
        dialog = BaseUI.crear_alerta(self, "Verificando Módulo de Cocción", "Esperando respuesta del Arduino...")

        def read_temperature():
            if not self.dialog_active:
                self.arduino_coccion.disconnect()  # Cerrar conexión si se interrumpe
                return

            response = self.arduino_coccion.read_response()
            if response:
                dialog.layout().itemAt(0).widget().setText(f"Temperatura actual: {response}°C")
                QTimer.singleShot(2000, lambda: self.finalizar_dialogo(dialog, self.arduino_coccion))
            else:
                QTimer.singleShot(500, read_temperature)

        read_temperature()
        dialog.exec_()

    def finalizar_dialogo(self, dialog, arduino):
        """Finaliza el diálogo y cierra la conexión serial."""
        dialog.accept()
        arduino.disconnect()
        self.dialog_active = False

    def regresar(self):
        self.dialog_active = False
        self.arduino_compresion.disconnect()
        self.arduino_coccion.disconnect()
        self.parent.setCurrentWidget(self.parent.pantalla_principal)
