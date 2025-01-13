from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class PantallaMasaDisponible(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.tortillas_calculadas = 0  # Inicializamos el número de tortillas calculadas
        self.init_ui()

    def init_ui(self):
        self.main_layout = QVBoxLayout()

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
        self.main_layout.addLayout(header_layout)

        # Cuerpo principal
        body_layout = QHBoxLayout()

        # Labels a la izquierda
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
        self.main_layout.addLayout(body_layout)

        self.setLayout(self.main_layout)

    def reset_pantalla(self):
        """
        Restaura el estado inicial de la pantalla.
        """
        self.label_bascula.setText("Peso Báscula: 0.0 kg")
        self.label_tortillas.setText("Tortillas Calculadas: 0")
        self.btn_tarar.setEnabled(True)
        self.btn_calcular.setEnabled(False)
        self.btn_iniciar.setEnabled(False)

    def tarar_bascula(self):
        self.btn_tarar.setEnabled(False)
        self.btn_calcular.setEnabled(True)

    def calcular_tortillas(self):
        # Simulación del cálculo
        self.label_bascula.setText("Peso Báscula: 2.0 kg")
        self.tortillas_calculadas = 60  # Simulación
        self.label_tortillas.setText(f"Tortillas Calculadas: {self.tortillas_calculadas}")
        self.btn_calcular.setEnabled(False)
        self.btn_iniciar.setEnabled(True)

    def iniciar(self):
        """
        Envía el número de tortillas calculadas a pantalla_operacion y cambia de pantalla.
        """
        self.parent.pantalla_operacion.actualizar_tortillas(self.tortillas_calculadas)
        self.parent.setCurrentWidget(self.parent.pantalla_operacion)

    def regresar(self):
        """
        Regresa a la pantalla principal.
        """
        self.parent.setCurrentWidget(self.parent.pantalla_automatico)
