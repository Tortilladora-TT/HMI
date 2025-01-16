from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer
from utils.base_ui import BaseUI
from utils.serial_manager import SerialManager
import RPi.GPIO as GPIO
from libraries.hx711py.hx711 import HX711
import logging
class PantallaTortillasDeseadas(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.hx = None  # Instancia de la báscula
        self.peso_actual = 0.0  # Peso inicial
        self.tortillas_disponibles = 0  # Tortillas posibles con la masa actual
        self.serial_pico = SerialManager(port='/dev/ttyUSB0', baudrate=9600)  # Configuración del puerto serial
        self.timer = QTimer()  # Inicialización del temporizador
        self.init_ui()

    def init_ui(self):
        # Configuración del layout principal
        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(40, 40, 40, 40)
        layout_principal.setSpacing(20)

        # Encabezado
        layout_principal.addWidget(BaseUI.crear_encabezado("Tortillas Deseadas"))
        layout_principal.addWidget(
            BaseUI.crear_subtitulo(
                "Instrucciones:\n"
                "1. Ingresa el número de tortillas.\n"
                "2. Guarda el valor.\n"
                "3. Coloca la masa.\n"
                "4. Observa la cantidad posible.\n"
                "5. Presiona Iniciar."
            )
        )

        # Cuerpo principal
        cuerpo_layout = QHBoxLayout()
        cuerpo_layout.setSpacing(30)

        # Sección izquierda: Displays
        display_layout = QVBoxLayout()
        display_layout.setSpacing(20)

        # Display para tortillas ingresadas
        self.input_value = QLabel("0")
        self.input_value.setFont(QFont("Arial", 24))
        self.input_value.setAlignment(Qt.AlignCenter)
        self.input_value.setStyleSheet("border: 2px solid black; padding: 10px;")
        display_layout.addWidget(BaseUI.crear_subtitulo("Tortillas Ingresadas"))
        display_layout.addWidget(self.input_value)

        # Display para tortillas disponibles
        self.available_value = QLabel("0")
        self.available_value.setFont(QFont("Arial", 24))
        self.available_value.setAlignment(Qt.AlignCenter)
        self.available_value.setStyleSheet("border: 2px solid black; padding: 10px;")
        display_layout.addWidget(BaseUI.crear_subtitulo("Tortillas Posibles"))
        display_layout.addWidget(self.available_value)

        cuerpo_layout.addLayout(display_layout)

        # Sección central: Teclado numérico
        teclado_layout = QGridLayout()
        teclado_layout.setSpacing(10)

        for i in range(1, 10):
            boton = BaseUI.crear_boton_numerico(str(i), lambda _, num=i: self.add_digit(num))
            teclado_layout.addWidget(boton, (i - 1) // 3, (i - 1) % 3)

        btn_clear = BaseUI.crear_boton_numerico("C", self.clear_input)
        teclado_layout.addWidget(btn_clear, 3, 0)

        btn_zero = BaseUI.crear_boton_numerico("0", lambda: self.add_digit(0))
        teclado_layout.addWidget(btn_zero, 3, 1)

        cuerpo_layout.addLayout(teclado_layout)

        # Sección derecha: Botones funcionales
        botones_layout = QVBoxLayout()
        botones_layout.setSpacing(20)

        btn_guardar = BaseUI.crear_boton("Guardar", self.guardar)
        botones_layout.addWidget(btn_guardar)

        self.btn_iniciar = BaseUI.crear_boton("Aceptar", self.iniciar)
        self.btn_iniciar.setEnabled(False)
        botones_layout.addWidget(self.btn_iniciar)

        btn_regresar = BaseUI.crear_boton("↩️ Regresar", self.regresar)
        botones_layout.addWidget(btn_regresar)

        cuerpo_layout.addLayout(botones_layout)
        layout_principal.addLayout(cuerpo_layout)

        self.setLayout(layout_principal)

    def reset_pantalla(self):
        """Reinicia el valor de las tortillas y desactiva el botón de inicio."""
        self.input_value.setText("0")
        self.available_value.setText("0")
        self.available_value.setStyleSheet("border: 2px solid black; padding: 10px; color: black;")
        self.btn_iniciar.setEnabled(False)
        self.stop_peso_update()
        if self.hx:
            try:
                self.hx.power_down()
                GPIO.cleanup()
            except Exception as e:
                print(f"Error al limpiar GPIO: {e}")
            self.hx = None

    def add_digit(self, digit):
        """Añade un dígito al valor actual."""
        current = self.input_value.text()
        if current == "0" or current == "ERROR":
            self.input_value.setText(str(digit))
        else:
            self.input_value.setText(current + str(digit))

    def clear_input(self):
        """Limpia el valor actual."""
        self.input_value.setText("0")

    def guardar(self):
        """Guarda el valor ingresado y habilita el botón iniciar."""
        try:
            tortillas = int(self.input_value.text())
            if tortillas < 1 or tortillas > 90:  # Limitamos a 90 tortillas
                self.input_value.setText("ERROR")
                self.btn_iniciar.setEnabled(False)
            else:
                self.btn_iniciar.setEnabled(True)
                self.start_peso_update()  # Inicia la actualización del peso
        except ValueError:
            self.input_value.setText("ERROR")
            self.btn_iniciar.setEnabled(False)

    def start_peso_update(self):
        """Inicia la actualización continua del peso."""
        if not self.hx:
            self.hx = HX711(5, 6)  # Pines DT y SCK
            self.hx.set_reference_unit(277)
            self.hx.reset()
            self.hx.tare()
        self.timer.timeout.connect(self.update_peso)
        self.timer.start(500)  # Actualiza cada 500 ms

    def stop_peso_update(self):
        """Detiene la actualización del peso."""
        if self.timer.isActive():
            self.timer.stop()

    def update_peso(self):
        """Actualiza el peso de la báscula y calcula las tortillas posibles."""
        try:
            self.peso_actual = abs(round(self.hx.get_weight(5) / 1000, 3))  # Peso en kg
            self.tortillas_disponibles = int(self.peso_actual * 30)  # Tortillas posibles
            self.available_value.setText(str(self.tortillas_disponibles))

            # Cambiar el color según las condiciones
            tortillas_ingresadas = int(self.input_value.text())
            if self.tortillas_disponibles < tortillas_ingresadas:
                self.available_value.setStyleSheet("border: 2px solid black; padding: 10px; color: red;")
            else:
                self.available_value.setStyleSheet("border: 2px solid black; padding: 10px; color: green;")
        except Exception as e:
            print(f"Error al leer el peso: {e}")
            self.available_value.setText("ERROR")
            self.available_value.setStyleSheet("border: 2px solid black; padding: 10px; color: black;")

    def iniciar(self):
        """Envía el número de tortillas ingresadas por serial y confirma el proceso."""
        try:
            tortillas = int(self.input_value.text())
            comando = f"pap {tortillas}"
            logging.info(f"Enviando comando: {comando}")
            self.serial_pico.connect()

            if self.serial_pico.connection:
                self.serial_pico.send_command(comando)
                logging.info("Comando enviado correctamente.")
                self.parent.cambiar_pantalla(self.parent.pantalla_operacion)
                self.parent.pantalla_operacion.actualizar_tortillas(tortillas)
            else:
                dialog = BaseUI.crear_alerta(self, "Error", "No se pudo conectar al módulo.")
                dialog.exec_()
                return

        except ValueError:
            logging.error("Error al convertir el valor ingresado.")
            self.input_value.setText("ERROR")
        except Exception as e:
            logging.error(f"Error al iniciar el proceso: {e}")
            dialog = BaseUI.crear_alerta(self, "Error", "Ocurrió un error al iniciar el proceso.")
            dialog.exec_()

    def regresar(self):
        """Regresa a la pantalla de modo automático."""
        self.reset_pantalla()
        self.parent.cambiar_pantalla(self.parent.pantalla_automatico)
