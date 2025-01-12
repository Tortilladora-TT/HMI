from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class PantallaOperacion(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.tortillas_label = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        titulo = QLabel("Operación en Proceso")
        titulo.setFont(QFont("Arial Black", 24))
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        self.tortillas_label = QLabel("Tortillas Calculadas: 0")
        self.tortillas_label.setFont(QFont("Arial", 18))
        self.tortillas_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.tortillas_label)

        btn_regresar = QPushButton("↩️ Regresar")
        btn_regresar.setFont(QFont("Arial", 14))
        btn_regresar.clicked.connect(self.regresar)
        layout.addWidget(btn_regresar)

        self.setLayout(layout)

    def actualizar_tortillas(self, cantidad):
        """
        Actualiza la etiqueta con la cantidad de tortillas calculadas.
        """
        self.tortillas_label.setText(f"Tortillas Calculadas: {cantidad}")

    def regresar(self):
        self.parent.setCurrentWidget(self.parent.pantalla_principal)