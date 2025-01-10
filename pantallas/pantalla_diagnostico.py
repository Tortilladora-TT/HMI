from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, QDialog
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer

class PantallaDiagnostico(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        # Configuración del layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Título
        titulo = QLabel("MODO DIAGNÓSTICO")
        titulo.setFont(QFont("Arial Black", 24))
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        # Subtítulo
        subtitulo = QLabel("Selecciona la opción que le gustaría verificar.\nRecuerda: este modo NO NECESITA MASA.")
        subtitulo.setFont(QFont("Arial", 14))
        subtitulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitulo)

        # Botones
        btn_dosificacion = QPushButton("DOSIFICACIÓN")
        btn_dosificacion.setFont(QFont("Arial", 16))
        btn_dosificacion.clicked.connect(self.dosificacion)
        layout.addWidget(btn_dosificacion)

        btn_compresion_corte = QPushButton("COMPRESIÓN Y CORTE")
        btn_compresion_corte.setFont(QFont("Arial", 16))
        btn_compresion_corte.clicked.connect(self.compresion_corte)
        layout.addWidget(btn_compresion_corte)

        btn_coccion = QPushButton("COCCIÓN")
        btn_coccion.setFont(QFont("Arial", 16))
        btn_coccion.clicked.connect(self.coccion)
        layout.addWidget(btn_coccion)

        # Botón para regresar
        btn_regresar = QPushButton("↩️ Regresar")
        btn_regresar.setFont(QFont("Arial", 14))
        btn_regresar.clicked.connect(self.regresar)
        layout.addWidget(btn_regresar)

        self.setLayout(layout)

    def dosificacion(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Verificando Módulo de Dosificación")
        dialog.setModal(True)
        dialog.setFixedSize(400, 200)

        layout = QVBoxLayout()
        label = QLabel("Esperando datos del módulo...")
        label.setFont(QFont("Arial", 14))
        layout.addWidget(label, alignment=Qt.AlignCenter)
        dialog.setLayout(layout)

        timer = QTimer(self)
        timer.setSingleShot(True)
        timer.timeout.connect(dialog.accept)  # Permite cerrar la ventana tras 5 segundos
        timer.start(5000)

        dialog.exec_()

    def compresion_corte(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Verificando Módulo de Compresión y Corte")
        dialog.setModal(True)
        dialog.setFixedSize(400, 300)

        layout = QVBoxLayout()
        label = QLabel("Verificando sensores...")
        label.setFont(QFont("Arial", 14))
        layout.addWidget(label, alignment=Qt.AlignCenter)
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
        dialog = QMessageBox(self)
        temperatura = "200"
        dialog.setWindowTitle("Verificando Módulo de Cocción")
        dialog.setText(f"Temperatura: {temperatura}°C")  # Cambia "200" por la variable con el formato apropiado
        dialog.setStandardButtons(QMessageBox.Close)
        dialog.exec_()

    def regresar(self):
        self.parent.setCurrentWidget(self.parent.pantalla_principal)
