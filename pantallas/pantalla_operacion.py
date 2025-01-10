from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PyQt5.QtGui import QFont


class PantallaOperacion(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        btn_regresar = QPushButton("↩️ Regresar")
        btn_regresar.setFont(QFont("Arial", 14))
        btn_regresar.clicked.connect(self.regresar)
        layout.addWidget(btn_regresar)

        self.setLayout(layout)

    def regresar(self):
        self.parent.setCurrentWidget(self.parent.pantalla_principal)