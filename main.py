from PyQt5.QtWidgets import QApplication, QStackedWidget
from pantallas.pantalla_principal import PantallaPrincipal
from pantallas.pantalla_diagnostico import PantallaDiagnostico
from pantallas.pantalla_automatico import PantallaAutomatico
from pantallas.pantalla_masa_disponible import PantallaMasaDisponible
from pantallas.pantalla_tortillas_deseadas import PantallaTortillasDeseadas
from pantallas.pantalla_operacion import PantallaOperacion
from PyQt5.QtCore import Qt
from config import cargar_estilos

class MainApp(QStackedWidget):
    def __init__(self):
        super().__init__()

        # Inicializar pantallas
        self.pantalla_masa_disponible = PantallaMasaDisponible(self)
        self.pantalla_tortillas_deseadas = PantallaTortillasDeseadas(self)
        self.pantalla_operacion = PantallaOperacion(self)
        self.pantalla_principal = PantallaPrincipal(self)
        self.pantalla_diagnostico = PantallaDiagnostico(self)
        self.pantalla_automatico = PantallaAutomatico(self)

        # Agregar pantallas al stack
        self.addWidget(self.pantalla_principal)
        self.addWidget(self.pantalla_diagnostico)
        self.addWidget(self.pantalla_automatico)
        self.addWidget(self.pantalla_masa_disponible)
        self.addWidget(self.pantalla_tortillas_deseadas)
        self.addWidget(self.pantalla_operacion)

        # Configuración de la ventana
        self.setWindowTitle("HMI - Selección de Modos")
        self.showFullScreen()  # Inicia en pantalla completa

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()  # Cerrar la aplicación si presionas Esc

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    # Cargar estilos
    cargar_estilos(app)

    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())
