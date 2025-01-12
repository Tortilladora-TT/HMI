from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
from utils.base_ui import BaseUI

class PantallaPrincipal(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        # Configuración del layout principal
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        # Título
        layout.addWidget(BaseUI.crear_encabezado("Selección de Modos"))

        # Subtítulo
        layout.addWidget(BaseUI.crear_subtitulo("Selecciona el modo de operación deseado"))

        # Espaciador para centrar los botones
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Botones principales
        botones_layout = QVBoxLayout()
        botones_layout.setAlignment(Qt.AlignCenter)
        botones_layout.setSpacing(15)

        botones_layout.addWidget(BaseUI.crear_boton("MODO AUTOMÁTICO", self.modo_automatico))
        botones_layout.addWidget(BaseUI.crear_boton("MODO DIAGNÓSTICO", self.modo_diagnostico))

        layout.addLayout(botones_layout)

        # Espaciador para mantener centrado
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(layout)

    def modo_automatico(self):
        self.parent.setCurrentWidget(self.parent.pantalla_automatico)

    def modo_diagnostico(self):
        self.parent.setCurrentWidget(self.parent.pantalla_diagnostico)
