from PyQt5.QtWidgets import QWidget, QVBoxLayout, QDialog, QLabel
from PyQt5.QtCore import Qt, QTimer
from utils.base_ui import BaseUI  # Usar la clase BaseUI para un diseño consistente

class PantallaDiagnostico(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        # Configuración del layout principal
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)  # Márgenes ajustados
        layout.setSpacing(20)  # Espaciado entre elementos

        # Título
        layout.addWidget(BaseUI.crear_encabezado("Modo Diagnóstico"))

        # Subtítulo
        layout.addWidget(BaseUI.crear_subtitulo("Selecciona la opción que le gustaría verificar.\nRecuerda: este modo es SIN MASA"))

        # Botones principales
        layout.addWidget(BaseUI.crear_boton("DOSIFICACIÓN", self.dosificacion))
        layout.addWidget(BaseUI.crear_boton("COMPRESIÓN Y CORTE", self.compresion_corte))
        layout.addWidget(BaseUI.crear_boton("COCCIÓN", self.coccion))

        # Botón para regresar
        layout.addWidget(BaseUI.crear_boton("↩️ Regresar", self.regresar))

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
