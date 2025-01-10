from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class PantallaAutomatico(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        # Configuración del layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Título
        titulo = QLabel("Modo Automático")
        titulo.setFont(QFont("Arial Black", 32))
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        # Subtítulo
        subtitulo = QLabel("Selecciona la opción según los datos que se van a ingresar")
        subtitulo.setFont(QFont("Arial", 18))
        subtitulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitulo)

        # Botones
        btn_masa_disponible = QPushButton("Masa Disponible")
        btn_masa_disponible.setFont(QFont("Arial", 16))
        btn_masa_disponible.clicked.connect(self.masa_disponible)
        layout.addWidget(btn_masa_disponible)

        btn_tortillas_deseadas = QPushButton("Tortillas Deseadas")
        btn_tortillas_deseadas.setFont(QFont("Arial", 16))
        btn_tortillas_deseadas.clicked.connect(self.tortillas_deseadas)
        layout.addWidget(btn_tortillas_deseadas)

        # Botón para regresar
        btn_regresar = QPushButton("↩️ Regresar")
        btn_regresar.setFont(QFont("Arial", 14))
        btn_regresar.clicked.connect(self.regresar)
        layout.addWidget(btn_regresar)

        self.setLayout(layout)

    def masa_disponible(self):
        print("Seleccionada la opción de Masa Disponible...")

    def tortillas_deseadas(self):
        print("Seleccionada la opción de Tortillas Deseadas...")

    def regresar(self):
        self.parent.setCurrentWidget(self.parent.pantalla_principal)
