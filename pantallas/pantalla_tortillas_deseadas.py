from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar, QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer
from utils.base_ui import BaseUI


class PantallaOperacion(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.total_tortillas = 0  # Total de tortillas deseadas
        self.tortillas_producidas = 0  # Tortillas producidas
        self.proceso_pausado = False
        self.timer = QTimer()  # Temporizador para simular la producción
        self.timer.timeout.connect(self.incrementar_produccion)  # Llama a incrementar_produccion cada vez que se activa
        self.init_ui()

    def init_ui(self):
        # Layout principal
        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(40, 40, 40, 40)
        layout_principal.setSpacing(20)

        # Encabezado
        layout_principal.addWidget(BaseUI.crear_encabezado("Operación en Proceso"))

        # Indicador de progreso
        self.tortillas_label = QLabel("Tortillas producidas: 0 / 0")
        self.tortillas_label.setFont(QFont("Arial", 18))
        self.tortillas_label.setAlignment(Qt.AlignCenter)
        layout_principal.addWidget(self.tortillas_label)

        # Barra de progreso personalizada
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setTextVisible(False)  # Eliminar texto del porcentaje
        layout_principal.addWidget(self.progress_bar)

        # Botones de control
        self.botones_layout = QHBoxLayout()
        self.botones_layout.setSpacing(20)

        self.btn_pausar = BaseUI.crear_boton("Pausar", self.toggle_pausa)
        self.botones_layout.addWidget(self.btn_pausar)

        self.btn_cancelar = BaseUI.crear_boton("Cancelar", self.cancelar)
        self.botones_layout.addWidget(self.btn_cancelar)

        layout_principal.addLayout(self.botones_layout)

        self.setLayout(layout_principal)

    def actualizar_tortillas(self, cantidad):
        """
        Actualiza el total de tortillas deseadas y reinicia el estado.
        """
        self.total_tortillas = cantidad
        self.tortillas_producidas = 0
        self.tortillas_label.setText(f"Tortillas producidas: 0 / {self.total_tortillas}")
        self.progress_bar.setValue(0)
        self.btn_pausar.setText("Pausar")
        self.btn_cancelar.setText("Cancelar")
        self.btn_cancelar.clicked.disconnect()  # Elimina la señal anterior
        self.btn_cancelar.clicked.connect(self.cancelar)  # Vuelve a conectar con "Cancelar"
        self.proceso_pausado = False
        self.timer.start(1000)  # Inicia el temporizador con intervalos de 1 segundo

    def incrementar_produccion(self):
        """
        Incrementa el conteo de tortillas producidas y actualiza la pantalla.
        Este método se llama periódicamente por el QTimer.
        """
        if not self.proceso_pausado and self.tortillas_producidas < self.total_tortillas:
            self.tortillas_producidas += 1
            progreso = int((self.tortillas_producidas / self.total_tortillas) * 100)
            self.tortillas_label.setText(
                f"Tortillas producidas: {self.tortillas_producidas} / {self.total_tortillas}"
            )
            self.progress_bar.setValue(progreso)

        if self.tortillas_producidas >= self.total_tortillas:
            self.finalizar_proceso()

    def finalizar_proceso(self):
        """
        Cambia la pantalla a modo 'Proceso terminado' y actualiza los botones.
        """
        self.timer.stop()  # Detiene el temporizador
        self.tortillas_label.setText("Proceso terminado")
        self.progress_bar.setValue(100)

        # Cambiar el botón "Cancelar" a "Finalizar"
        self.btn_cancelar.setText("Finalizar")
        self.btn_cancelar.clicked.disconnect()  # Desconectar señal anterior
        self.btn_cancelar.clicked.connect(self.finalizar)

        # Deshabilitar el botón "Pausar"
        self.btn_pausar.setEnabled(False)

    def toggle_pausa(self):
        """
        Pausa o reanuda el proceso según el estado actual.
        """
        if self.proceso_pausado:
            self.proceso_pausado = False
            self.btn_pausar.setText("Pausar")
        else:
            self.proceso_pausado = True
            self.btn_pausar.setText("Reanudar")

    def cancelar(self):
        """
        Cancela el proceso y regresa al menú principal.
        """
        self.timer.stop()  # Detiene el temporizador
        self.parent.cambiar_pantalla(self.parent.pantalla_principal)

    def finalizar(self):
        """
        Finaliza el proceso y regresa al menú principal.
        """
        self.parent.cambiar_pantalla(self.parent.pantalla_principal)
