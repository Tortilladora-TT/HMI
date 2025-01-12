from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
from utils.base_ui import BaseUI

class PantallaAutomatico(QWidget):
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
        layout.addWidget(BaseUI.crear_encabezado("Modo Automático"))

        # Subtítulo
        layout.addWidget(BaseUI.crear_subtitulo("Selecciona la opción según los datos que se van a ingresar"))

        # Espaciador para centrar los botones
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Botones principales
        botones_layout = QVBoxLayout()
        botones_layout.setAlignment(Qt.AlignCenter)
        botones_layout.setSpacing(15)

        botones_layout.addWidget(BaseUI.crear_boton("Masa Disponible", self.masa_disponible))
        botones_layout.addWidget(BaseUI.crear_boton("Tortillas Deseadas", self.tortillas_deseadas))

        layout.addLayout(botones_layout)

        # Espaciador para mantener centrado
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Botón para regresar
        layout.addWidget(BaseUI.crear_boton("↩️ Regresar", self.regresar), alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def masa_disponible(self):
        self.parent.setCurrentWidget(self.parent.pantalla_masa_disponible)

    def tortillas_deseadas(self):
        self.parent.setCurrentWidget(self.parent.pantalla_tortillas_deseadas)

    def regresar(self):
        self.parent.setCurrentWidget(self.parent.pantalla_principal)
