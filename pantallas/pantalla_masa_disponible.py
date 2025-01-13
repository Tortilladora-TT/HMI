from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from utils.base_ui import BaseUI  # Reutilizamos el estilo de encabezados y botones

class PantallaMasaDisponible(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.tortillas_calculadas = 0  # Inicializamos el número de tortillas calculadas
        self.init_ui()

    def init_ui(self):
        # Configuración del layout principal
        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(40, 40, 40, 40)
        layout_principal.setSpacing(20)

        # Encabezado
        layout_principal.addWidget(BaseUI.crear_encabezado("Masa Disponible"))
        layout_principal.addWidget(
            BaseUI.crear_subtitulo(
                "Instrucciones:\n"
                "1. Tarar báscula.\n"
                "2. Coloca la masa.\n"
                "3. Calcula número de tortillas.\n"
                "4. Presiona Iniciar."
            )
        )

        # Cuerpo principal
        cuerpo_layout = QHBoxLayout()
        cuerpo_layout.setSpacing(30)

        # Sección izquierda: Labels dinámicos
        labels_layout = QVBoxLayout()
        labels_layout.setSpacing(15)
        self.label_bascula = QLabel("Peso Báscula: 0.0 kg")
        self.label_bascula.setFont(QFont("Arial", 18))
        self.label_bascula.setAlignment(Qt.AlignLeft)
        labels_layout.addWidget(self.label_bascula)

        self.label_tortillas = QLabel("Tortillas Calculadas: 0")
        self.label_tortillas.setFont(QFont("Arial", 18))
        self.label_tortillas.setAlignment(Qt.AlignLeft)
        labels_layout.addWidget(self.label_tortillas)

        cuerpo_layout.addLayout(labels_layout)

        # Sección derecha: Botones
        botones_layout = QVBoxLayout()
        botones_layout.setSpacing(20)

        self.btn_tarar = BaseUI.crear_boton("Tarar Báscula", self.tarar_bascula)
        botones_layout.addWidget(self.btn_tarar)

        self.btn_calcular = BaseUI.crear_boton("Calcular Tortillas", self.calcular_tortillas)
        self.btn_calcular.setEnabled(False)  # Inicia desactivado
        botones_layout.addWidget(self.btn_calcular)

        self.btn_iniciar = BaseUI.crear_boton("Iniciar", self.iniciar)
        self.btn_iniciar.setEnabled(False)  # Inicia desactivado
        botones_layout.addWidget(self.btn_iniciar)

        cuerpo_layout.addLayout(botones_layout)
        layout_principal.addLayout(cuerpo_layout)

        # Espaciador y botón de regresar
        layout_principal.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        layout_principal.addWidget(
            BaseUI.crear_boton("↩️ Regresar", self.regresar), alignment=Qt.AlignRight
        )

        self.setLayout(layout_principal)

    def reset_pantalla(self):
        """
        Restaura el estado inicial de la pantalla.
        """
        self.label_bascula.setText("Peso Báscula: 0.0 kg")
        self.label_tortillas.setText("Tortillas Calculadas: 0")
        self.tortillas_calculadas = 0
        self.btn_tarar.setEnabled(True)
        self.btn_calcular.setEnabled(False)
        self.btn_iniciar.setEnabled(False)

    def tarar_bascula(self):
        """Simula el tarado de la báscula."""
        self.btn_tarar.setEnabled(False)
        self.btn_calcular.setEnabled(True)

    def calcular_tortillas(self):
        """Simula el cálculo de tortillas basado en el peso."""
        self.label_bascula.setText("Peso Báscula: 2.0 kg")
        self.tortillas_calculadas = 60  # Simulación
        self.label_tortillas.setText(f"Tortillas Calculadas: {self.tortillas_calculadas}")
        self.btn_calcular.setEnabled(False)
        self.btn_iniciar.setEnabled(True)

    def iniciar(self):
        """Envía el número de tortillas calculadas a pantalla_operacion y cambia de pantalla."""
        self.parent.pantalla_operacion.actualizar_tortillas(self.tortillas_calculadas)
        self.parent.cambiar_pantalla(self.parent.pantalla_operacion)

    def regresar(self):
        """Regresa a la pantalla anterior y reinicia el estado."""
        #self.reset_pantalla()
        self.parent.cambiar_pantalla(self.parent.pantalla_automatico)
