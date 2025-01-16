from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt, QTimer
from utils.base_ui import BaseUI
from utils.serial_manager import SerialManager
import logging

class PantallaDiagnostico(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.dialog_active = False  # Control para evitar múltiples diálogos activos
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
        pico = SerialManager(port='/dev/ttyUSB0', baudrate=9600)  # Conexión local
        pico.connect()

        if not pico.connection:
            dialog = BaseUI.crear_alerta(self, "Error", "No se pudo conectar al módulo de dosificación.")
            dialog.exec_()
            return

        # Enviar el comando "dd"
        pico.send_command("dd")
        logging.info("Comando 'dd' enviado a la Pico.")

        dialog = BaseUI.crear_alerta(self, "Verificando Módulo de Dosificación", "Ejecutando diagnóstico...")
        dialog.setModal(True)

        def check_status():
            response = pico.read_response()
            if response:
                dialog.layout().itemAt(0).widget().setText(f"Respuesta: {response}")
                if response == "Done":
                    QTimer.singleShot(2000, lambda: self.finalizar_dialogo(dialog, pico))
                else:
                    QTimer.singleShot(500, check_status)
            else:
                dialog.layout().itemAt(0).widget().setText("Verificando Módulo de Dosificación...")
                QTimer.singleShot(500, check_status)

        check_status()
        dialog.exec_()

    def compresion_corte(self):
        logging.info("Iniciando diagnóstico del módulo de compresión y corte")
        arduino = SerialManager(port='/dev/ttyUSB1', baudrate=9600)  # Conexión local
        arduino.connect()

        if not arduino.connection:
            dialog = BaseUI.crear_alerta(self, "Error", "No se pudo conectar al módulo de compresión y corte.")
            dialog.exec_()
            return

        arduino.send_command("dcc")
        dialog = BaseUI.crear_alerta(self, "Verificando Módulo de Compresión y Corte", "Esperando respuesta del Arduino...")

        def read_response():
            response = arduino.read_response()
            if response:
                dialog.layout().itemAt(0).widget().setText("Verificando Módulo de Compresión y Corte")
                #QTimer.singleShot(2000, lambda: self.finalizar_dialogo(dialog, arduino))
            else:
                dialog.layout().itemAt(0).widget().setText("Esperando respuesta...")
                QTimer.singleShot(500, read_response)

        read_response()
        dialog.exec_()

    def coccion(self):
        logging.info("Iniciando diagnóstico del módulo de cocción")
        #arduino = SerialManager(port='/dev/AMA0', baudrate=9600)  # Conexión local
        #arduino.connect()

        #if not arduino.connection:
            #dialog = BaseUI.crear_alerta(self, "Error", "No se pudo conectar al módulo de cocción.")
            #dialog.exec_()
            #return

        #arduino.send_command("D")
        #dialog = BaseUI.crear_alerta(self, "Verificando Módulo de Cocción", "Temperatura actual: 90.15°C")
        #dialog.layout().itemAt(0).widget().setText("Verificando Módulo de Compresión y Corte")
        #def read_temperature():
            #response = arduino.read_response()
            #if response:
        #dialog.layout().itemAt(0).widget().setText("Temperatura actual: 90.15°C")
                #QTimer.singleShot(2000, lambda: self.finalizar_dialogo(dialog, arduino))
            #else:
                #dialog.layout().itemAt(0).widget().setText("Esperando respuesta...")
                #QTimer.singleShot(500, read_temperature)

        #read_temperature()
        #dialog.exec_()
        # Crear y mostrar el diálogo
        dialog = BaseUI.crear_alerta(self, "Verificando Módulo de Cocción", "Verificando módulo de cocción...")
        dialog.exec_()

    def finalizar_dialogo(self, dialog, arduino):
        """Finaliza el diálogo y cierra la conexión serial."""
        dialog.accept()
        arduino.disconnect()

    def regresar(self):
        self.parent.setCurrentWidget(self.parent.pantalla_principal)
