from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
from utils.base_ui import BaseUI

class PantallaPrincipal(QWidget):
    def __init__(self, parent, width, height):
        super().__init__()
        self.parent = parent
        self.width = width
        self.height = height
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(
            int(self.width * 0.05),
            int(self.height * 0.05),
            int(self.width * 0.05),
            int(self.height * 0.05)
        )
        layout.setSpacing(int(self.height * 0.02))

        # Título
        layout.addWidget(BaseUI.crear_encabezado("Selección de Modos"))

        # Espaciador pequeño debajo del título
        layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Subtítulo
        layout.addWidget(BaseUI.crear_subtitulo("Selecciona el modo de operación deseado"))

        # Espaciador para centrar los botones principales
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Botones principales
        botones_layout = QVBoxLayout()
        botones_layout.setAlignment(Qt.AlignCenter)
        botones_layout.setSpacing(15)

        botones_layout.addWidget(BaseUI.crear_boton("MODO AUTOMÁTICO", self.modo_automatico))
        botones_layout.addWidget(BaseUI.crear_boton("MODO DIAGNÓSTICO", self.modo_diagnostico))

        layout.addLayout(botones_layout)

        # Espaciador para separar el botón de regresar de los botones principales
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(layout)

    def modo_automatico(self):
        self.parent.setCurrentWidget(self.parent.pantalla_automatico)

    def modo_diagnostico(self):
        self.parent.setCurrentWidget(self.parent.pantalla_diagnostico)
