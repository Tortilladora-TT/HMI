from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer
from utils.base_ui import BaseUI
import RPi.GPIO as GPIO
import sys
import time
from libraries.hx711py.hx711 import HX711

class PantallaMasaDisponible(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.tortillas_calculadas = 0  # Inicializamos el número de tortillas calculadas
        self.hx = None  # Instancia de la báscula
        self.peso_actual = 0.0  # Peso inicial
        self.init_ui()

    def init_ui(self):
        # Layout principal
        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(40, 40, 40, 40)
        layout_principal.setSpacing(20)

        # Encabezado
        layout_principal.addWidget(BaseUI.crear_encabezado("Masa Disponible"))

        # Subtítulo dinámico
        self.subtitulo = BaseUI.crear_subtitulo("Presiona el botón tarar para calibrar la báscula.")
        layout_principal.addWidget(self.subtitulo)

        # Labels dinámicos
        labels_layout = QVBoxLayout()
        self.label_bascula = QLabel("Peso Báscula: 0.0 kg")
        self.label_bascula.setFont(QFont("Arial", 18))
        self.label_bascula.setAlignment(Qt.AlignCenter)
        self.label_bascula.setStyleSheet("border: 2px solid black; padding: 10px;")
        labels_layout.addWidget(self.label_bascula)

        self.label_tortillas = QLabel("Tortillas Calculadas: 0")
        self.label_tortillas.setFont(QFont("Arial", 18))
        self.label_tortillas.setAlignment(Qt.AlignCenter)
        self.label_tortillas.setStyleSheet("border: 2px solid black; padding: 10px;")
        labels_layout.addWidget(self.label_tortillas)

        layout_principal.addLayout(labels_layout)

        # Botones en una matriz 2x2
        botones_layout = QGridLayout()
        botones_layout.setSpacing(20)

        # Fila 1
        self.btn_tarar = BaseUI.crear_boton("Tarar Báscula", self.tarar_bascula)
        botones_layout.addWidget(self.btn_tarar, 0, 0)

        self.btn_guardar = BaseUI.crear_boton("Guardar", self.guardar_peso)
        self.btn_guardar.setEnabled(False)  # Inicia desactivado
        botones_layout.addWidget(self.btn_guardar, 0, 1)

        # Fila 2
        self.btn_iniciar = BaseUI.crear_boton("Iniciar", self.iniciar)
        self.btn_iniciar.setEnabled(False)  # Inicia desactivado
        botones_layout.addWidget(self.btn_iniciar, 1, 0)

        btn_regresar = BaseUI.crear_boton("↩️ Regresar", self.regresar)
        botones_layout.addWidget(btn_regresar, 1, 1)

        layout_principal.addLayout(botones_layout)

        self.setLayout(layout_principal)

        # Iniciar la actualización continua del peso
        self.start_peso_update()

    def reset_pantalla(self):
        """Restaura el estado inicial de la pantalla y limpia los GPIO."""
        self.label_bascula.setText("Peso Báscula: 0.0 kg")
        self.label_tortillas.setText("Tortillas Calculadas: 0")
        self.btn_tarar.setEnabled(True)
        self.btn_guardar.setEnabled(False)
        self.btn_iniciar.setEnabled(False)
        self.subtitulo.setText("Presiona el botón tarar para calibrar la báscula.")
        if self.hx:
            GPIO.cleanup()  # Limpia los GPIO

    def tarar_bascula(self):
        """Configura y realiza la tara de la báscula."""
        try:
            self.hx = HX711(5, 6)  # Pines DT y SCK
            self.hx.set_reference_unit(277)  # Unidad de referencia
            self.hx.reset()
            self.hx.tare()  # Realiza la tara
            self.subtitulo.setText("Báscula tarada. Ahora coloca la masa.")
            self.btn_tarar.setEnabled(False)
            self.btn_guardar.setEnabled(True)
        except Exception as e:
            self.subtitulo.setText("Error al tarar la báscula.")
            print(f"Error: {e}")

    def start_peso_update(self):
        """Actualiza el peso de la báscula continuamente en el label."""
        try:
            if self.hx:
                self.peso_actual = self.hx.get_weight(5) / 1000  # Obtener peso en kg
                self.peso_actual = round(self.peso_actual, 3)  # Redondear a 3 decimales
                self.label_bascula.setText(f"Peso Báscula: {self.peso_actual} kg")
                self.label_tortillas.setText(
                    f"Tortillas Calculadas: {int(self.peso_actual * 30)}"
                )  # Actualiza el cálculo de tortillas
        except Exception as e:
            self.label_bascula.setText("Peso Báscula: Error")
            print(f"Error al leer el peso: {e}")

        # Continuar actualizando cada 500ms
        QTimer.singleShot(500, self.start_peso_update)

    def guardar_peso(self):
        """Guarda el peso actual y habilita el botón iniciar."""
        try:
            self.tortillas_calculadas = int(self.peso_actual * 30)  # 1 kg = 30 tortillas
            self.btn_iniciar.setEnabled(True)
            self.subtitulo.setText("Peso guardado. Puedes ajustar si es necesario.")
        except Exception as e:
            print(f"Error al guardar el peso: {e}")

    def iniciar(self):
        """Envía el número de tortillas calculadas a pantalla_operacion y cambia de pantalla."""
        self.parent.pantalla_operacion.actualizar_tortillas(self.tortillas_calculadas)
        self.parent.cambiar_pantalla(self.parent.pantalla_operacion)

    def regresar(self):
        """Regresa a la pantalla anterior, limpia los GPIO y reinicia el estado."""
        self.reset_pantalla()
        self.parent.cambiar_pantalla(self.parent.pantalla_automatico)
