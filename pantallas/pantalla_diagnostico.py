from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSpacerItem, QSizePolicy, QDialog, QLabel
from PyQt5.QtCore import Qt, QTimer
from utils.base_ui import BaseUI

class PantallaDiagnostico(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        # Configuración del layout principal
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)  # Márgenes ajustados a 40px
        layout.setSpacing(20)

        # Título
        layout.addWidget(BaseUI.crear_encabezado("Modo Diagnóstico"))

        # Espaciador pequeño debajo del título
        layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Subtítulo
        layout.addWidget(BaseUI.crear_subtitulo("Selecciona la opción que le gustaría verificar.\nRecuerda: este modo es SIN MASA"))

        # Espaciador para centrar los botones principales
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Botones principales
        botones_layout = QVBoxLayout()
        botones_layout.setAlignment(Qt.AlignCenter)
        botones_layout.setSpacing(15)

        botones_layout.addWidget(BaseUI.crear_boton("DOSIFICACIÓN", self.dosificacion))
        botones_layout.addWidget(BaseUI.crear_boton("COMPRESIÓN Y CORTE", self.compresion_corte))
        botones_layout.addWidget(BaseUI.crear_boton("COCCIÓN", self.coccion))

        layout.addLayout(botones_layout)

        # Espaciador para separar el botón de regresar de los botones principales
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Botón para regresar
        layout.addWidget(BaseUI.crear_boton("↩️ Regresar", self.regresar), alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def dosificacion(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Verificando Módulo de Dosificación")
        dialog.setModal(True)
        dialog.setFixedSize(400, 200)

        layout = QVBoxLayout()
        label = QLabel("Esperando datos del módulo...")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        dialog.setLayout(layout)

        timer = QTimer(self)
        timer.setSingleShot(True)
        timer.timeout.connect(dialog.accept)
        timer.start(5000)

        dialog.exec_()

    def compresion_corte(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Verificando Módulo de Compresión y Corte")
        dialog.setModal(True)
        dialog.setFixedSize(400, 200)

        layout = QVBoxLayout()
        label = QLabel("Verificando sensores...")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        dialog.setLayout(layout)

        sensor_texts = [
            "Sensor Recepción validado",
            "Sensor Corte 1 validado",
            "Sensor Corte 2 validado",
            "Sensor Compresión validado",
            "Sensor Expulsión validado",
        ]

        def update_label(i=0):
            if i < len(sensor_texts):
                label.setText(sensor_texts[i])
                QTimer.singleShot(3000, lambda: update_label(i + 1))
            else:
                dialog.accept()

        update_label()
        dialog.exec_()

    def coccion(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Verificando Módulo de Cocción")
        dialog.setModal(True)
        dialog.setFixedSize(400, 200)

        layout = QVBoxLayout()
        temperatura = "200"  # Aquí entra el valor de la temperatura
        label = QLabel(f"Temperatura: {temperatura}°C")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        dialog.setLayout(layout)

        dialog.exec_()

    def regresar(self):
        self.parent.setCurrentWidget(self.parent.pantalla_principal)
