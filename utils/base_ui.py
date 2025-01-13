from PyQt5.QtWidgets import QLabel, QPushButton, QDialog, QVBoxLayout
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

    @staticmethod
    def crear_boton_numerico(texto, funcion):
        """Crea un QPushButton estilizado para teclas numéricas."""
        boton = QPushButton(texto)
        boton.setFont(QFont("Arial", 20))
        boton.setFixedHeight(60)
        boton.setFixedWidth(60)
        boton.clicked.connect(funcion)
        return boton
    
    @staticmethod
    def crear_alerta(parent, titulo, mensaje, ancho=400, alto=200):
        """Crea un QDialog estilizado para mostrar alertas."""
        dialog = QDialog(parent)
        dialog.setWindowTitle(titulo)
        dialog.setModal(True)
        dialog.setFixedSize(ancho, alto)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # Mensaje principal
        label = QLabel(mensaje)
        label.setFont(QFont("Arial", 16))  # Fuente estándar para alertas
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        dialog.setLayout(layout)
        return dialog
