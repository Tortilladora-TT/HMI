from PyQt5.QtWidgets import QWidget, QVBoxLayout
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
        layout.setAlignment(Qt.AlignCenter)  # Alinear todo al centro
        layout.setContentsMargins(0, 0, 0, 0)  # Sin márgenes
        layout.setSpacing(20)  # Espaciado entre elementos

        # Encabezado
        layout.addWidget(BaseUI.crear_encabezado("Modo Automático"))

        # Subtítulo
        layout.addWidget(BaseUI.crear_subtitulo("Selecciona la opción según los datos que se van a ingresar"))

        # Botones principales
        layout.addWidget(BaseUI.crear_boton("Masa Disponible", self.masa_disponible))
        layout.addWidget(BaseUI.crear_boton("Tortillas Deseadas", self.tortillas_deseadas))

        # Botón para regresar
        layout.addWidget(BaseUI.crear_boton("↩️ Regresar", self.regresar))

        self.setLayout(layout)

    def masa_disponible(self):
        self.parent.setCurrentWidget(self.parent.pantalla_masa_disponible)

    def tortillas_deseadas(self):
        self.parent.setCurrentWidget(self.parent.pantalla_tortillas_deseadas)

    def regresar(self):
        self.parent.setCurrentWidget(self.parent.pantalla_principal)
