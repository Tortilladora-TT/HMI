from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class PantallaPrincipal(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        titulo = QLabel("Selección de Modos")
        titulo.setFont(QFont("Arial Black", 32))
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        subtitulo = QLabel("Selecciona el modo de operación deseado")
        subtitulo.setFont(QFont("Arial", 18))
        subtitulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitulo)

        btn_automatico = QPushButton("MODO AUTOMÁTICO")
        btn_automatico.clicked.connect(self.modo_automatico)
        layout.addWidget(btn_automatico)

        btn_diagnostico = QPushButton("MODO DIAGNÓSTICO")
        btn_diagnostico.clicked.connect(self.modo_diagnostico)
        layout.addWidget(btn_diagnostico)

        self.setLayout(layout)

    def modo_automatico(self):
        print("Entrando al Modo Automático...")

    def modo_diagnostico(self):
        self.parent.setCurrentWidget(self.parent.pantalla_diagnostico)