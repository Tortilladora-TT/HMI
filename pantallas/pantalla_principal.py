from PyQt5.QtWidgets import QWidget, QVBoxLayout
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
        layout.setAlignment(Qt.AlignCenter)  # Alinear todos los elementos al centro
        layout.setContentsMargins(0, 0, 0, 0)  # Sin márgenes adicionales
        layout.setSpacing(20)  # Espaciado vertical entre elementos

        # Encabezado
        layout.addWidget(BaseUI.crear_encabezado("Selección de Modos"))

        # Subtítulo
        layout.addWidget(BaseUI.crear_subtitulo("Selecciona el modo de operación deseado"))

        # Botones principales
        layout.addWidget(BaseUI.crear_boton("MODO AUTOMÁTICO", self.modo_automatico))
        layout.addWidget(BaseUI.crear_boton("MODO DIAGNÓSTICO", self.modo_diagnostico))

        self.setLayout(layout)

    def modo_automatico(self):
        self.parent.setCurrentWidget(self.parent.pantalla_automatico)

    def modo_diagnostico(self):
        self.parent.setCurrentWidget(self.parent.pantalla_diagnostico)
