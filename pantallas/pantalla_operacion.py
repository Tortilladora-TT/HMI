from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar, QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer
from utils.base_ui import BaseUI
from utils.serial_manager import SerialManager
import logging
import time


class PantallaOperacion(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.total_tortillas = 0  # Total de tortillas deseadas
        self.tortillas_producidas = 0  # Tortillas producidas
        self.timer = QTimer()  # Temporizador para actualizar la barra de progreso
        self.timer.timeout.connect(self.control_produccion)
        self.serial_pico = SerialManager(port='/dev/ttyUSB0', baudrate=9600)
        self.serial_nano = SerialManager(port='/dev/ttyUSB1', baudrate=9600)
        self.init_ui()

    def init_ui(self):
        # Layout principal
        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(40, 40, 40, 40)
        layout_principal.setSpacing(20)

        # Encabezado
        layout_principal.addWidget(BaseUI.crear_encabezado("Operación en Proceso"))

        # Indicador de progreso
        self.tortillas_label = QLabel("Tortillas producidas: 0 / 0")
        self.tortillas_label.setFont(QFont("Arial", 18))
        self.tortillas_label.setAlignment(Qt.AlignCenter)
        layout_principal.addWidget(self.tortillas_label)

        # Barra de progreso personalizada
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setMaximum(100)
        layout_principal.addWidget(self.progress_bar)

        # Botones de control
        self.botones_layout = QHBoxLayout()
        self.botones_layout.setSpacing(20)

        self.btn_iniciar = BaseUI.crear_boton("Iniciar", self.iniciar_produccion)
        self.botones_layout.addWidget(self.btn_iniciar)

        self.btn_cancelar = BaseUI.crear_boton("Cancelar", self.cancelar)
        self.botones_layout.addWidget(self.btn_cancelar)

        layout_principal.addLayout(self.botones_layout)

        self.setLayout(layout_principal)

    def actualizar_tortillas(self, cantidad):
        """
        Actualiza el total de tortillas deseadas y reinicia el estado.
        """
        self.total_tortillas = cantidad
        self.tortillas_producidas = 0
        self.tortillas_label.setText(f"Tortillas producidas: 0 / {self.total_tortillas}")
        self.progress_bar.setValue(0)
        self.btn_iniciar.setEnabled(True)  # Rehabilitar el botón de iniciar
        self.btn_cancelar.setText("Cancelar")

    def iniciar_produccion(self):
        """
        Inicia el ciclo de producción interactuando con los microcontroladores.
        """
        self.btn_iniciar.setEnabled(False)  # Inhabilitar el botón de inicio
        try:
            self.serial_pico.connect()
            self.serial_nano.connect()

            if not self.serial_pico.connection or not self.serial_nano.connection:
                dialog = BaseUI.crear_alerta(
                    self, "Error", "No se pudo conectar con uno o más microcontroladores."
                )
                dialog.exec_()
                return

            logging.info("Iniciando ciclo de producción.")
            self.timer.start(1000)  # Actualizar cada segundo
        except Exception as e:
            logging.error(f"Error al iniciar la producción: {e}")
            dialog = BaseUI.crear_alerta(self, "Error", f"Ocurrió un error: {e}")
            dialog.exec_()

    def control_produccion(self):
        """
        Controla la interacción entre la Pico y el Nano.
        """
        try:
            if self.tortillas_producidas < self.total_tortillas:
                # Enviar comando a la Pico
                self.serial_pico.send_command("ad")
                response_pico = self.serial_pico.read_response()

                if response_pico == "Testal":
                    logging.info("Respuesta 'Testal' recibida de la Pico.")
                    
                    if self.serial_nano.connection:
                        time.sleep(0.1)  # Breve pausa antes de enviar el comando
                        self.serial_nano.send_command("Iniciar")
                        logging.info("Comando 'Iniciar' enviado al Nano.")
                        
                        response_nano = self.serial_nano.read_response()
                        if response_nano == "Tortilla":
                            logging.info("Respuesta 'Tortilla' recibida del Nano.")
                            self.tortillas_producidas += 1
                            progreso = int((self.tortillas_producidas / self.total_tortillas) * 100)
                            self.tortillas_label.setText(
                                f"Tortillas producidas: {self.tortillas_producidas} / {self.total_tortillas}"
                            )
                            self.progress_bar.setValue(progreso)
                            
                            # Enviar comando para detener el motor
                            self.serial_pico.send_command("Alto")
                            logging.info("Comando 'Stop' enviado a la Pico.")
                            
                            QTimer.singleShot(5000, self.control_produccion)  # Reintentar después de 5 segundos
                        else:
                            logging.warning(f"Respuesta inesperada del Nano: {response_nano}")
                    else:
                        logging.error("Conexión con el Nano no disponible.")

            else:
                self.finalizar_proceso()
        except Exception as e:
            logging.error(f"Error durante ciclo de producción: {e}")
            dialog = BaseUI.crear_alerta(self, "Error", f"Ocurrió un error: {e}")
            dialog.exec_()

    def finalizar_proceso(self):
        """
        Cambia la pantalla a modo 'Proceso terminado' y actualiza los botones.
        """
        self.timer.stop()  # Detener el temporizador
        self.tortillas_label.setText("Proceso terminado")
        self.progress_bar.setValue(100)
        self.btn_cancelar.setText("Finalizar")
        self.btn_cancelar.clicked.disconnect()
        self.btn_cancelar.clicked.connect(self.finalizar)

    def cancelar(self):
        """
        Cancela el proceso y regresa al menú principal.
        """
        self.timer.stop()  # Detener el temporizador
        self.serial_pico.send_command("Alto")
        self.serial_nano.send_command("Alto")
        self.parent.cambiar_pantalla(self.parent.pantalla_principal)

    def finalizar(self):
        """
        Finaliza el proceso y regresa al menú principal.
        """
        self.serial_pico.send_command("Alto")
        self.serial_nano.send_command("Alto")
        self.parent.cambiar_pantalla(self.parent.pantalla_principal)
