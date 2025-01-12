from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QGridLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class PantallaTortillasDeseadas(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # Título
        titulo = QLabel("Tortillas Deseadas")
        titulo.setFont(QFont("Arial Black", 24))
        titulo.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(titulo)

        # Instrucciones
        subtitulo = QLabel("Instrucciones:\n"
                           "1. Ingresa el número de tortillas.\n"
                           "2. Guarda el valor.\n"
                           "3. Coloca la masa.\n"
                           "4. Presiona Iniciar.")
        subtitulo.setFont(QFont("Arial", 14))
        subtitulo.setAlignment(Qt.AlignLeft)
        main_layout.addWidget(subtitulo)

        # Layout principal
        body_layout = QHBoxLayout()

        # Teclado numérico
        teclado_layout = QGridLayout()
        self.input_value = QLabel("0")
        self.input_value.setFont(QFont("Arial", 20))
        self.input_value.setAlignment(Qt.AlignCenter)
        body_layout.addWidget(self.input_value)

        # Generar teclas
        for i in range(1, 10):
            button = QPushButton(str(i))
            button.setFont(QFont("Arial", 20))
            button.clicked.connect(lambda _, num=i: self.add_digit(num))
            teclado_layout.addWidget(button, (i - 1) // 3, (i - 1) % 3)

        btn_clear = QPushButton("C")
        btn_clear.setFont(QFont("Arial", 20))
        btn_clear.clicked.connect(self.clear_input)
        teclado_layout.addWidget(btn_clear, 3, 0)

        btn_zero = QPushButton("0")
        btn_zero.setFont(QFont("Arial", 20))
        btn_zero.clicked.connect(lambda: self.add_digit(0))
        teclado_layout.addWidget(btn_zero, 3, 1)

        body_layout.addLayout(teclado_layout)

        # Botones funcionales
        buttons_layout = QVBoxLayout()
        btn_guardar = QPushButton("Guardar")
        btn_guardar.setFont(QFont("Arial", 16))
        btn_guardar.clicked.connect(self.guardar)
        buttons_layout.addWidget(btn_guardar)

        self.btn_iniciar = QPushButton("Iniciar")
        self.btn_iniciar.setFont(QFont("Arial", 16))
        self.btn_iniciar.setEnabled(False)
        self.btn_iniciar.clicked.connect(self.iniciar)
        buttons_layout.addWidget(self.btn_iniciar)

        btn_regresar = QPushButton("↩️ Regresar")
        btn_regresar.setFont(QFont("Arial", 16))
        btn_regresar.clicked.connect(self.regresar)
        buttons_layout.addWidget(btn_regresar)

        body_layout.addLayout(buttons_layout)
        main_layout.addLayout(body_layout)

        self.setLayout(main_layout)

    def add_digit(self, digit):
        current = self.input_value.text()
        if current == "0":
            self.input_value.setText(str(digit))
        else:
            self.input_value.setText(current + str(digit))

    def clear_input(self):
        self.input_value.setText("0")

    def guardar(self):
        try:
            tortillas = int(self.input_value.text())
            if tortillas < 30 and tortillas > 90:
                self.input_value.setText("ERROR")
                self.input_value.setText("0")
            else:
                self.btn_iniciar.setEnabled(True)
        except ValueError:
            self.input_value.setText("ERROR")

    def iniciar(self):
        self.parent.setCurrentWidget(self.parent.pantalla_operacion)

    def regresar(self):
        self.parent.setCurrentWidget(self.parent.pantalla_automatico)
