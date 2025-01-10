from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from animated_button import AnimatedButton

class PantallaPrincipal(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        # Configuración del layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Título
        titulo = QLabel("Selección de Modos")
        titulo.setFont(QFont("Arial Black", 24))
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        # Subtítulo
        subtitulo = QLabel("Selecciona el modo de operación deseado")
        subtitulo.setFont(QFont("Arial", 14))
        subtitulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitulo)

        # Botones
        btn_automatico = QPushButton("MODO AUTOMÁTICO")
        btn_automatico.setFont(QFont("Arial", 16))
        btn_automatico.setStyleSheet("background-color: #88cffa; border-radius: 15px; padding: 15px;")
        btn_automatico.clicked.connect(self.modo_automatico)
        layout.addWidget(btn_automatico)

        btn_diagnostico = QPushButton("MODO DIAGNÓSTICO")
        btn_diagnostico.setFont(QFont("Arial", 16))
        btn_diagnostico.setStyleSheet("background-color: #ffa8a8; border-radius: 15px; padding: 15px;")
        btn_diagnostico.clicked.connect(self.modo_diagnostico)
        layout.addWidget(btn_diagnostico)

        self.setLayout(layout)

    def modo_automatico(self):
        print("Entrando al Modo Automático...")

    def modo_diagnostico(self):
        self.parent.setCurrentWidget(self.parent.pantalla_diagnostico)
