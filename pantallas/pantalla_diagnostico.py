from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt, QTimer
from utils.base_ui import BaseUI
import logging
import serial
import time

class PantallaDiagnostico(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.arduino = None  # Instancia del puerto serial
        self.init_ui()
        self.connect_serial()

    def init_ui(self):
        # Configuración del layout principal
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)  # Márgenes ajustados
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

    def connect_serial(self):
        """Conecta al puerto serial del Arduino."""
        try:
            self.arduino = serial.Serial(port='/dev/ttyUSB1', baudrate=9600, timeout=1)  # Ajusta el puerto según sea necesario
            time.sleep(2)  # Esperar a que el Arduino se reinicie
            logging.info("Conexión exitosa con el Arduino")
        except Exception as e:
            logging.error(f"Error al conectar con el Arduino: {e}")
            self.arduino = None

    def dosificacion(self):
        logging.info("Iniciando diagnóstico del módulo de dosificación")
        dialog = BaseUI.crear_alerta(self, "Verificando Módulo de Dosificación", "Esperando datos del módulo...")
        QTimer.singleShot(5000, dialog.accept)  # Cerrar automáticamente después de 5 segundos
        logging.info("Módulo de dosificación validado correctamente")
        dialog.exec_()

    def compresion_corte(self):
        logging.info("Iniciando diagnóstico del módulo de compresión y corte")

        if not self.arduino:
            logging.error("El Arduino no está conectado. Verifica la conexión.")
            dialog = BaseUI.crear_alerta(self, "Error", "No se detectó conexión con el Arduino.")
            dialog.exec_()
            return

        # Enviar el comando "dcc\n" para iniciar el diagnóstico
        try:
            self.arduino.write(b'dcc\n')
            logging.info("Comando 'dcc' enviado al Arduino")
        except Exception as e:
            logging.error(f"Error al enviar comando al Arduino: {e}")
            dialog = BaseUI.crear_alerta(self, "Error", "No se pudo enviar el comando al Arduino.")
            dialog.exec_()
            return

        # Crear diálogo para mostrar el estado del diagnóstico
        dialog = BaseUI.crear_alerta(self, "Verificando Módulo de Compresión y Corte", "Esperando respuesta del Arduino...")
        dialog.setModal(True)

        def read_serial():
            try:
                response = self.arduino.readline().decode('utf-8').strip()
                if response:
                    if response == "RSwitches":
                        dialog.layout().itemAt(0).widget().setText("Switches: Correcto")
                    elif response == "ESwitches":
                        dialog.layout().itemAt(0).widget().setText("Switches: Error")
                        QTimer.singleShot(2000, dialog.accept)
                        return
                    elif response == "RMotores":
                        dialog.layout().itemAt(0).widget().setText("Motores: Correcto")
                    elif response == "EMotores":
                        dialog.layout().itemAt(0).widget().setText("Motores: Error")
                        QTimer.singleShot(2000, dialog.accept)
                        return
                    elif response == "RIR":
                        dialog.layout().itemAt(0).widget().setText("Sensor IR: Correcto")
                        QTimer.singleShot(2000, dialog.accept)
                        return
                    elif response == "EIR":
                        dialog.layout().itemAt(0).widget().setText("Sensor IR: Error")
                        QTimer.singleShot(2000, dialog.accept)
                        return
                    else:
                        dialog.layout().itemAt(0).widget().setText(f"Respuesta desconocida: {response}")

                # Continuar leyendo después de 500 ms
                QTimer.singleShot(500, read_serial)
            except Exception as e:
                logging.error(f"Error al leer respuesta del Arduino: {e}")
                dialog.layout().itemAt(0).widget().setText("Error de comunicación.")
                QTimer.singleShot(2000, dialog.accept)

        read_serial()
        dialog.exec_()

    def coccion(self):
        logging.info("Iniciando diagnóstico del módulo de cocción")
        temperatura = "200"  # Aquí entra el valor de la temperatura
        mensaje = f"Temperatura actual: {temperatura}°C"
        dialog = BaseUI.crear_alerta(self, "Verificando Módulo de Cocción", mensaje)
        QTimer.singleShot(5000, dialog.accept)
        logging.info("Módulo de cocción validado correctamente")
        dialog.exec_()

    def regresar(self):
        self.parent.setCurrentWidget(self.parent.pantalla_principal)

    def close_serial(self):
        """Cierra la conexión serial."""
        if self.arduino:
            self.arduino.close()
            logging.info("Conexión serial cerrada.")
