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
        self.proceso_pausado = False
        self.proceso_iniciado = False  # El proceso no ha comenzado
        self.timer = QTimer()  # Temporizador para manejar el proceso
        self.timer.timeout.connect(self.ciclo_produccion)  # Llama a ciclo_produccion
        self.serial_pico = SerialManager(port='/dev/USB0', baudrate=9600)
        self.serial_nano = SerialManager(port='/dev/USB1', baudrate=9600)
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
        self.progress_bar.setTextVisible(False)
        layout_principal.addWidget(self.progress_bar)

        # Botones de control
        self.botones_layout = QHBoxLayout()
        self.botones_layout.setSpacing(20)

        self.btn_iniciar_pausar = BaseUI.crear_boton("Iniciar", self.toggle_iniciar_pausar)
        self.botones_layout.addWidget(self.btn_iniciar_pausar)

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
        self.proceso_iniciado = False
        self.proceso_pausado = False
        self.btn_iniciar_pausar.setText("Iniciar")
        self.btn_cancelar.setText("Cancelar")
        self.btn_cancelar.clicked.disconnect()
        self.btn_cancelar.clicked.connect(self.cancelar)

    def ciclo_produccion(self):
        """
        Controla el ciclo de producción:
        - Interacción entre la Pico y el Nano.
        - Incrementa el contador al recibir los datos correctos.
        """
        if self.proceso_pausado:
            return

        try:
            if not self.serial_pico.connection:
                self.serial_pico.connect()
            if not self.serial_nano.connection:
                self.serial_nano.connect()

            # Enviar "ad" a la Pico para iniciar el ciclo
            logging.info("Enviando 'ad' a la Pico.")
            self.serial_pico.send_command("ad")
            logging.info("Esperando 'Testal' de la Pico.")
            response_pico = self.serial_pico.read_response(timeout=10)
            if response_pico == "Testal":
                logging.info("'Testal' recibido, enviando 'Iniciar' al Nano.")
                self.serial_nano.send_command("Iniciar")
                response_nano = self.serial_nano.read_response(timeout=10)

                if response_nano == "Tortilla":
                    self.tortillas_producidas += 1
                    progreso = int((self.tortillas_producidas / self.total_tortillas) * 100)
                    self.tortillas_label.setText(
                        f"Tortillas producidas: {self.tortillas_producidas} / {self.total_tortillas}"
                    )
                    self.progress_bar.setValue(progreso)

                    if self.tortillas_producidas >= self.total_tortillas:
                        self.finalizar_proceso()
                    else:
                        logging.info("Esperando 5 segundos antes de iniciar el siguiente ciclo.")
                        time.sleep(5)

        except Exception as e:
            logging.error(f"Error durante el ciclo de producción: {e}")

    def toggle_iniciar_pausar(self):
        """
        Maneja la lógica del botón "Iniciar/Pausar".
        """
        if not self.proceso_iniciado:  # Estado inicial: Iniciar
            self.proceso_iniciado = True
            self.proceso_pausado = False
            self.btn_iniciar_pausar.setText("Pausar")
            self.timer.start(1000)
            logging.info("Proceso iniciado.")
        else:
            if self.proceso_pausado:  # Reanudar
                self.proceso_pausado = False
                self.btn_iniciar_pausar.setText("Pausar")
                logging.info("Proceso reanudado.")
            else:  # Pausar
                self.proceso_pausado = True
                self.btn_iniciar_pausar.setText("Reanudar")
                logging.info("Proceso pausado.")

    def finalizar_proceso(self):
        """
        Cambia la pantalla a modo 'Proceso terminado' y actualiza los botones.
        """
        self.timer.stop()
        self.tortillas_label.setText("Proceso terminado")
        self.progress_bar.setValue(100)
        self.btn_cancelar.setText("Finalizar")
        self.btn_cancelar.clicked.disconnect()
        self.btn_cancelar.clicked.connect(self.finalizar)
        self.btn_iniciar_pausar.setEnabled(False)

    def cancelar(self):
        """
        Cancela el proceso y regresa al menú principal.
        """
        self.timer.stop()
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
