# base_ui.py
from PyQt5.QtWidgets import QLabel, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class BaseUI:
    @staticmethod
    def crear_encabezado(texto):
        """Crea un QLabel estilizado para títulos."""
        encabezado = QLabel(texto)
        encabezado.setFont(QFont("Arial Black", 28))  # Tamaño equilibrado
        encabezado.setAlignment(Qt.AlignCenter)
        return encabezado

    @staticmethod
    def crear_subtitulo(texto):
        """Crea un QLabel estilizado para subtítulos."""
        subtitulo = QLabel(texto)
        subtitulo.setFont(QFont("Arial", 18))  # Tamaño estándar para subtítulos
        subtitulo.setAlignment(Qt.AlignCenter)
        return subtitulo

    @staticmethod
    def crear_boton(texto, funcion):
        """Crea un QPushButton estilizado."""
        boton = QPushButton(texto)
        boton.setFont(QFont("Arial", 20))  # Tamaño adecuado para pantallas táctiles
        boton.setFixedHeight(80)          # Altura mayor para pantallas táctiles
        boton.setFixedWidth(400)          # Más ancho para facilidad de toque
        boton.clicked.connect(funcion)
        return boton