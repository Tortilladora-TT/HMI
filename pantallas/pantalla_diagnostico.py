from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt, QTimer
from utils.base_ui import BaseUI
import logging

class PantallaDiagnostico(QWidget):
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
        layout.addWidget(BaseUI.crear_encabezado("Modo Diagnóstico"))

        # Subtítulo
        layout.addWidget(BaseUI.crear_subtitulo("Selecciona la opción que le gustaría verificar.\nRecuerda: este modo es SIN MASA"))

        # Espaciador superior para separar el texto de los botones
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Botones principales
        botones_layout = QVBoxLayout()
        botones_layout.setAlignment(Qt.AlignCenter)
        botones_layout.setSpacing(15)

        # Botones añadidos al layout
        botones_layout.addWidget(BaseUI.crear_boton("DOSIFICACIÓN", self.dosificacion))
        botones_layout.addWidget(BaseUI.crear_boton("COMPRESIÓN Y CORTE", self.compresion_corte))
        botones_layout.addWidget(BaseUI.crear_boton("COCCIÓN", self.coccion))

        # Añadir layout de botones al layout principal
        layout.addLayout(botones_layout)

        # Espaciador inferior para el botón de regresar
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Botón para regresar
        layout.addWidget(BaseUI.crear_boton("↩️ Regresar", self.regresar), alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def dosificacion(self):
        logging.info("Iniciando diagnóstico del módulo de dosificación")
        dialog = BaseUI.crear_alerta(self, "Verificando Módulo de Dosificación", "Esperando datos del módulo...")
        QTimer.singleShot(5000, dialog.accept)  # Cerrar automáticamente después de 5 segundos
        logging.info("Módulo de dosificación validado correctamente")
        dialog.exec_()

    def compresion_corte(self):
        logging.info("Iniciando diagnóstico del módulo de compresión y corte")
        dialog = BaseUI.crear_alerta(self, "Verificando Módulo de Compresión y Corte", "Verificando sensores...")
        sensor_texts = [
            "Sensor Recepción validado",
            "Sensor Corte 1 validado",
            "Sensor Corte 2 validado",
            "Sensor Compresión validado",
            "Sensor Expulsión validado",
        ]

        def update_label(i=0):
            if i < len(sensor_texts):
                dialog.layout().itemAt(0).widget().setText(sensor_texts[i])
                QTimer.singleShot(3000, lambda: update_label(i + 1))
            else:
                dialog.accept()

        update_label()
        logging.info("Módulo de compresión y corte validado correctamente")
        dialog.exec_()

    def coccion(self):
        logging.info("Iniciando diagnóstico del módulo de cocción")
        temperatura = "200"  # Aquí entra el valor de la temperatura
        mensaje = f"Temperatura actual: {temperatura}°C"
        dialog = BaseUI.crear_alerta(self, "Verificando Módulo de Cocción", mensaje)
        QTimer.singleShot(5000, dialog.accept)
        logging.info("Módulo de cocción validado correctamente")
        dialog.exec_()

    def regresar(self):
        self.parent.setCurrentWidget(self.parent.pantalla_principal)
