from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class PantallaDiagnostico(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        titulo = QLabel("MODO DIAGNÓSTICO")
        titulo.setFont(QFont("Arial Black", 32))
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        subtitulo = QLabel("Selecciona la opción que le gustaría verificar.\nRecuerda: este modo NO NECESITA MASA.")
        subtitulo.setFont(QFont("Arial", 18))
        subtitulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitulo)

        btn_dosificacion = QPushButton("DOSIFICACIÓN")
        btn_dosificacion.clicked.connect(self.dosificacion)
        layout.addWidget(btn_dosificacion)

        btn_corte = QPushButton("CORTE")
        btn_corte.clicked.connect(self.corte)
        layout.addWidget(btn_corte)

        btn_compresion = QPushButton("COMPRESIÓN Y COCCIÓN")
        btn_compresion.clicked.connect(self.compresion)
        layout.addWidget(btn_compresion)

        btn_regresar = QPushButton("↩️ Regresar")
        btn_regresar.clicked.connect(self.regresar)
        layout.addWidget(btn_regresar)

        self.setLayout(layout)

    def dosificacion(self):
        print("Verificando el sistema de dosificación...")

    def corte(self):
        print("Verificando el sistema de corte...")

    def compresion(self):
        print("Verificando el sistema de compresión y cocción...")

    def regresar(self):
        self.parent.setCurrentWidget(self.parent.pantalla_principal)