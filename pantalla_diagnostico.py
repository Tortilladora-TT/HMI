from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from animated_button import AnimatedButton


class PantallaDiagnostico(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        # Configuración del layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Título
        titulo = QLabel("MODO DIAGNÓSTICO")
        titulo.setFont(QFont("Arial Black", 24))
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        # Subtítulo
        subtitulo = QLabel("Selecciona la opción que le gustaría verificar.\nRecuerda: este modo NO NECESITA MASA.")
        subtitulo.setFont(QFont("Arial", 14))
        subtitulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitulo)

        # Botones
        btn_dosificacion = QPushButton("DOSIFICACIÓN")
        btn_dosificacion.setFont(QFont("Arial", 16))
        btn_dosificacion.setStyleSheet("background-color: #e4c1f9; border-radius: 15px; padding: 15px;")
        btn_dosificacion.clicked.connect(self.dosificacion)
        layout.addWidget(btn_dosificacion)

        btn_corte = QPushButton("CORTE")
        btn_corte.setFont(QFont("Arial", 16))
        btn_corte.setStyleSheet("background-color: #f9e4c1; border-radius: 15px; padding: 15px;")
        btn_corte.clicked.connect(self.corte)
        layout.addWidget(btn_corte)

        btn_compresion = QPushButton("COMPRESIÓN Y COCCIÓN")
        btn_compresion.setFont(QFont("Arial", 16))
        btn_compresion.setStyleSheet("background-color: #c1f9e4; border-radius: 15px; padding: 15px;")
        btn_compresion.clicked.connect(self.compresion)
        layout.addWidget(btn_compresion)

        # Botón para regresar
        btn_regresar = QPushButton("↩️ Regresar")
        btn_regresar.setFont(QFont("Arial", 14))
        btn_regresar.setStyleSheet("background-color: #d4ffcc; border-radius: 15px; padding: 10px;")
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
