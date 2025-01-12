import serial
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QDialog
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer

class PantallaDiagnostico(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        titulo = QLabel("MODO DIAGNÓSTICO")
        titulo.setFont(QFont("Arial Black", 24))
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        subtitulo = QLabel("Selecciona la opción que le gustaría verificar.\nRecuerda: este modo NO NECESITA MASA.")
        subtitulo.setFont(QFont("Arial", 14))
        subtitulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitulo)

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

        btn_regresar = QPushButton("↩️ Regresar")
        btn_regresar.setFont(QFont("Arial", 14))
        btn_regresar.clicked.connect(self.regresar)
        layout.addWidget(btn_regresar)

        self.setLayout(layout)

    def serial_setup(self, port):
        return serial.Serial(port, baudrate=9600, timeout=1)

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

        port = self.serial_setup("/dev/USB0")
        port.write(b"diag_dos")

        def read_serial():
            if port.in_waiting:
                data = port.readline().decode().strip()
                label.setText(data)
            else:
                QTimer.singleShot(1000, read_serial)

        QTimer.singleShot(1000, read_serial)
        dialog.exec_()
        port.close()

    def compresion_corte(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Verificando Módulo de Compresión y Corte")
        dialog.setModal(True)
        dialog.setFixedSize(400, 200)

        layout = QVBoxLayout()
        label = QLabel("Verificando sensores...")
        label.setFont(QFont("Arial", 14))
        layout.addWidget(label, alignment=Qt.AlignCenter)
        dialog.setLayout(layout)

        sensor_map = {
            "ckrp": "Sensor Recepción validado",
            "ckc1": "Sensor Corte 1 validado",
            "ckc2": "Sensor Corte 2 validado",
            "ckcp": "Sensor Compresión validado",
            "ckex": "Sensor Expulsión validado"
        }

        port = self.serial_setup("/dev/USB1")
        port.write(b"diag_com")

        def read_serial():
            if port.in_waiting:
                data = port.readline().decode().strip()
                if data in sensor_map:
                    label.setText(sensor_map[data])
                if label.text() == "Sensor Expulsión validado":
                    dialog.accept()
            else:
                QTimer.singleShot(1000, read_serial)

        QTimer.singleShot(1000, read_serial)
        dialog.exec_()
        port.close()

    def coccion(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Verificando Módulo de Cocción")
        dialog.setModal(True)
        dialog.setFixedSize(400, 200)

        layout = QVBoxLayout()
        label = QLabel("Esperando datos de temperatura...")
        label.setFont(QFont("Arial", 14))
        layout.addWidget(label, alignment=Qt.AlignCenter)
        dialog.setLayout(layout)

        port = self.serial_setup("/dev/AMA0")
        port.write(b"diag_coc")

        def read_serial():
            if port.in_waiting:
                data = port.readline().decode().strip()
                if data.isdigit():
                    label.setText(f"Temperatura: {int(data)}°C")
            QTimer.singleShot(3000, read_serial)

        QTimer.singleShot(3000, read_serial)
        dialog.exec_()
        port.close()

    def regresar(self):
        self.parent.setCurrentWidget(self.parent.pantalla_principal)
