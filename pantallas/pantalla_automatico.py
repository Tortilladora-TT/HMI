from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
from utils.base_ui import BaseUI

class PantallaAutomatico(QWidget):
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
        layout.addWidget(BaseUI.crear_encabezado("Modo Automático"))

        # Espaciador pequeño debajo del título
        layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Subtítulo
        layout.addWidget(BaseUI.crear_subtitulo("Selecciona la opción según los datos que se van a ingresar"))

        # Espaciador para centrar los botones principales
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Botones principales
        botones_layout = QVBoxLayout()
        botones_layout.setAlignment(Qt.AlignCenter)
        botones_layout.setSpacing(15)

        botones_layout.addWidget(BaseUI.crear_boton("MASA DISPONIBLE", self.masa_disponible))
        botones_layout.addWidget(BaseUI.crear_boton("TORTILLAS DESEADAS", self.tortillas_deseadas))

        layout.addLayout(botones_layout)

        # Espaciador para separar el botón de regresar de los botones principales
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Botón para regresar
        layout.addWidget(BaseUI.crear_boton("↩️ Regresar", self.regresar), alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def masa_disponible(self):
        self.parent.setCurrentWidget(self.parent.pantalla_masa_disponible)
        self.parent.pantalla_masa_disponible.reset_pantalla()

    def tortillas_deseadas(self):
        self.parent.setCurrentWidget(self.parent.pantalla_tortillas_deseadas)

    def regresar(self):
        self.parent.setCurrentWidget(self.parent.pantalla_principal)
