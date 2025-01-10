from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QPropertyAnimation, QRect

class AnimatedButton(QPushButton):
    def __init__(self, label):
        super().__init__(label)
        self.setStyleSheet(
            """
            background-color: #88cffa;
            border-radius: 15px;
            font-size: 16px;
            font-weight: bold;
            padding: 15px;
            """
        )
        self.setFixedSize(300, 100)  # Tamaño fijo

    def enterEvent(self, event):
        self.setStyleSheet(
            """
            background-color: #72b6d4;
            border-radius: 15px;
            font-size: 16px;
            font-weight: bold;
            padding: 15px;
            """
        )
        self.animate_button(scale=1.05)  # Leve agrandamiento al pasar el cursor

    def leaveEvent(self, event):
        self.setStyleSheet(
            """
            background-color: #88cffa;
            border-radius: 15px;
            font-size: 16px;
            font-weight: bold;
            padding: 15px;
            """
        )
        self.animate_button(scale=1.0)  # Vuelve al tamaño normal

    def animate_button(self, scale):
        # Tamaño actual del botón
        width = self.width()
        height = self.height()

        # Cálculo del tamaño escalado
        scaled_width = int(width * scale)
        scaled_height = int(height * scale)

        # Mantener la posición centrada
        x = self.x() - (scaled_width - width) // 2
        y = self.y() - (scaled_height - height) // 2

        # Animación
        animation = QPropertyAnimation(self, b"geometry")
        animation.setDuration(200)  # Duración rápida para interacción fluida
        animation.setStartValue(self.geometry())  # Tamaño inicial
        animation.setEndValue(QRect(x, y, scaled_width, scaled_height))  # Tamaño final
        animation.start()
