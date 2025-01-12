from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QDialog
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer
from hx711 import HX711
import RPi.GPIO as GPIO

class PantallaMasaDisponible(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.hx = HX711(5, 6)  # Pines GPIO: DT = 5, SCK = 6
        self.init_ui()
        self.setup_hx711()

    def setup_hx711(self):
        # Configuración inicial de la báscula
        self.hx.set_reading_format("MSB", "MSB")
        reference_unit = 283.29  # Ajustar según calibración
        self.hx.set_reference_unit(reference_unit)
        self.hx.reset()
        self.hx.tare()  # Tarea inicial

    def init_ui(self):
        main_layout = QVBoxLayout()

        # Encabezado
        header_layout = QVBoxLayout()
        titulo = QLabel("Masa Disponible")
        titulo.setFont(QFont("Arial Black", 24))
        titulo.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(titulo)

        subtitulo = QLabel("Instrucciones:\n"
                           "1. Tarar báscula.\n"
                           "2. Coloca la masa.\n"
                           "3. Calcula número de tortillas.\n"
                           "4. Presiona Iniciar.")
        subtitulo.setFont(QFont("Arial", 14))
        subtitulo.setAlignment(Qt.AlignLeft)
        header_layout.addWidget(subtitulo)
        main_layout.addLayout(header_layout)

        # Cuerpo principal
        body_layout = QHBoxLayout()

        # Labels en la izquierda
        labels_layout = QVBoxLayout()
        self.label_bascula = QLabel("Peso Báscula: 0.0 kg")
        self.label_bascula.setFont(QFont("Arial", 18))
        self.label_tortillas = QLabel("Tortillas Calculadas: 0")
        self.label_tortillas.setFont(QFont("Arial", 18))
        labels_layout.addWidget(self.label_bascula)
        labels_layout.addWidget(self.label_tortillas)
        body_layout.addLayout(labels_layout)

        # Botones a la derecha
        buttons_layout = QVBoxLayout()
        self.btn_tarar = QPushButton("Tarar Báscula")
        self.btn_tarar.setFont(QFont("Arial", 16))
        self.btn_tarar.clicked.connect(self.tarar_bascula)
        buttons_layout.addWidget(self.btn_tarar)

        self.btn_calcular = QPushButton("Calcular Tortillas")
        self.btn_calcular.setFont(QFont("Arial", 16))
        self.btn_calcular.setEnabled(False)
        self.btn_calcular.clicked.connect(self.calcular_tortillas)
        buttons_layout.addWidget(self.btn_calcular)

        self.btn_iniciar = QPushButton("Iniciar")
        self.btn_iniciar.setFont(QFont("Arial", 16))
        self.btn_iniciar.setEnabled(False)
        self.btn_iniciar.clicked.connect(self.iniciar)
        buttons_layout.addWidget(self.btn_iniciar)

        # Botón regresar
        btn_regresar = QPushButton("↩️ Regresar")
        btn_regresar.setFont(QFont("Arial", 16))
        btn_regresar.clicked.connect(self.regresar)
        buttons_layout.addWidget(btn_regresar)

        body_layout.addLayout(buttons_layout)
        main_layout.addLayout(body_layout)

        self.setLayout(main_layout)

    def tarar_bascula(self):
        self.hx.tare()  # Realiza la tara
        self.label_bascula.setText("Peso Báscula: 0.0 kg")
        self.btn_tarar.setEnabled(False)
        self.btn_calcular.setEnabled(True)

    def calcular_tortillas(self):
        try:
            peso = round(self.hx.get_weight(5) / 1000, 3)  # Conversión a kg
            self.label_bascula.setText(f"Peso Báscula: {peso} kg")

            # Suponiendo que cada tortilla requiere 33g de masa
            tortillas = int((peso * 1000) / 33)
            self.label_tortillas.setText(f"Tortillas Calculadas: {tortillas}")

            self.btn_calcular.setEnabled(False)
            self.btn_iniciar.setEnabled(True)
        except Exception as e:
            dialog = QDialog(self)
            dialog.setWindowTitle("Error")
            dialog.setFixedSize(300, 150)
            layout = QVBoxLayout()
            label = QLabel(f"Error al leer la báscula: {e}")
            layout.addWidget(label)
            dialog.setLayout(layout)
            dialog.exec_()

    def iniciar(self):
        self.parent.setCurrentWidget(self.parent.pantalla_operacion)

    def regresar(self):
        self.parent.setCurrentWidget(self.parent.pantalla_automatico)