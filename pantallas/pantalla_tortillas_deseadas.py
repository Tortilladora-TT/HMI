from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from utils.base_ui import BaseUI


class PantallaTortillasDeseadas(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        # Configuración del layout principal
        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(40, 40, 40, 40)
        layout_principal.setSpacing(20)

        # Encabezado
        layout_principal.addWidget(BaseUI.crear_encabezado("Tortillas Deseadas"))
        layout_principal.addWidget(
            BaseUI.crear_subtitulo(
                "Instrucciones:\n"
                "1. Ingresa el número de tortillas.\n"
                "2. Guarda el valor.\n"
                "3. Coloca la masa.\n"
                "4. Presiona Iniciar."
            )
        )

        # Cuerpo principal
        cuerpo_layout = QHBoxLayout()
        cuerpo_layout.setSpacing(30)

        # Sección izquierda: Display del número de tortillas
        display_layout = QVBoxLayout()
        display_layout.setSpacing(20)

        self.input_value = QLabel("0")
        self.input_value.setFont(QFont("Arial", 24))
        self.input_value.setAlignment(Qt.AlignCenter)
        self.input_value.setStyleSheet("border: 2px solid black; padding: 10px;")
        display_layout.addWidget(self.input_value)

        cuerpo_layout.addLayout(display_layout)

        # Sección central: Teclado numérico
        teclado_layout = QGridLayout()
        teclado_layout.setSpacing(10)

        for i in range(1, 10):
            boton = BaseUI.crear_boton_numerico(str(i), lambda _, num=i: self.add_digit(num))
            teclado_layout.addWidget(boton, (i - 1) // 3, (i - 1) % 3)

        btn_clear = BaseUI.crear_boton_numerico("C", self.clear_input)
        teclado_layout.addWidget(btn_clear, 3, 0)

        btn_zero = BaseUI.crear_boton_numerico("0", lambda: self.add_digit(0))
        teclado_layout.addWidget(btn_zero, 3, 1)

        cuerpo_layout.addLayout(teclado_layout)

        # Sección derecha: Botones funcionales
        botones_layout = QVBoxLayout()
        botones_layout.setSpacing(20)

        btn_guardar = BaseUI.crear_boton("Guardar", self.guardar)
        botones_layout.addWidget(btn_guardar)

        self.btn_iniciar = BaseUI.crear_boton("Iniciar", self.iniciar)
        self.btn_iniciar.setEnabled(False)
        botones_layout.addWidget(self.btn_iniciar)

        btn_regresar = BaseUI.crear_boton("↩️ Regresar", self.regresar)
        botones_layout.addWidget(btn_regresar)

        cuerpo_layout.addLayout(botones_layout)
        layout_principal.addLayout(cuerpo_layout)

        self.setLayout(layout_principal)

    def add_digit(self, digit):
        """Añade un dígito al valor actual."""
        current = self.input_value.text()
        if current == "0" or current == "ERROR":
            self.input_value.setText(str(digit))
        else:
            self.input_value.setText(current + str(digit))

    def clear_input(self):
        """Limpia el valor actual."""
        self.input_value.setText("0")

    def guardar(self):
        """Guarda el valor ingresado."""
        try:
            tortillas = int(self.input_value.text())
            if tortillas > 90:  # Limitamos a 90 tortillas
                self.input_value.setText("ERROR")
                self.btn_iniciar.setEnabled(False)
            else:
                self.btn_iniciar.setEnabled(True)
        except ValueError:
            self.input_value.setText("ERROR")
            self.btn_iniciar.setEnabled(False)

    def iniciar(self):
        """Envía el valor a pantalla_operacion y cambia de pantalla."""
        try:
            tortillas = int(self.input_value.text())
            self.parent.pantalla_operacion.actualizar_tortillas(tortillas)
            self.parent.cambiar_pantalla(self.parent.pantalla_operacion)
        except ValueError:
            self.input_value.setText("ERROR")

    def regresar(self):
        """Regresa a la pantalla de modo automático."""
        self.parent.cambiar_pantalla(self.parent.pantalla_automatico)
