from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QGuiApplication

def obtener_resolucion():
    screen = QGuiApplication.primaryScreen()
    size = screen.size()
    return size.width(), size.height()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)  # Necesario para inicializar el sistema gráfico
    width, height = obtener_resolucion()
    print(f"Resolución detectada: {width}x{height}")
