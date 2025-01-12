from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from hx711 import HX711
import RPi.GPIO as GPIO

class SensorThread(QThread):
    peso_actualizado = pyqtSignal(float)

    def __init__(self, hx):
        super().__init__()
        self.hx = hx
        self.running = True

    def run(self):
        while self.running:
            try:
                peso = self.hx.get_weight(5) / 1000  # Convertir a kg
                self.peso_actualizado.emit(round(peso, 3))
                self.hx.power_down()
                self.hx.power_up()
                self.msleep(500)  # Leer cada 500 ms
            except Exception as e:
                print(f"Error al leer el sensor: {e}")

    def detener(self):
        self.running = False
        self.wait()

class PantallaMasaDisponible(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_sensor()
        self.init_ui()

    def init_sensor(self):
        GPIO.setwarnings(False)
        self.hx = HX711(5, 6)  # Pines DT y SCK
        self.hx.set_reference_unit(283.29)
        self.hx.reset()
        self.hx.tare()
        self.sensor_thread = SensorThread(self.hx)
        self.sensor_thread.peso_actualizado.connect(self.actualizar_peso)
        self.peso_actual = 0.0

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
        self.hx.tare()
        self.label_bascula.setText("Peso Báscula: 0.0 kg")
        self.btn_tarar.setEnabled(False)
        self.btn_calcular.setEnabled(True)
        self.sensor_thread.start()

    def calcular_tortillas(self):
        self.btn_calcular.setEnabled(False)
        self.btn_iniciar.setEnabled(True)
        tortillas = int(self.peso_actual / 0.033)  # Suponiendo 33 g por tortilla
        self.label_tortillas.setText(f"Tortillas Calculadas: {tortillas}")

    def actualizar_peso(self, peso):
        self.peso_actual = peso
        self.label_bascula.setText(f"Peso Báscula: {peso} kg")

    def iniciar(self):
        self.sensor_thread.detener()
        self.parent.setCurrentWidget(self.parent.pantalla_operacion)

    def regresar(self):
        self.sensor_thread.detener()
        self.parent.setCurrentWidget(self.parent.pantalla_automatico)
