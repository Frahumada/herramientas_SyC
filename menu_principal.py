from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from utils.estilos import btn_blue, btn_green, btn_red,ventana_principal_style

class MenuPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Menú Principal")
        self.setGeometry(100, 100, 500, 400)
        self.setStyleSheet(ventana_principal_style)

        layout = QVBoxLayout()

        titulo = QLabel("Selecciona un proceso")
        titulo.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titulo)

        self.btn_comparar = QPushButton("Comparar Nombres")
        self.btn_comparar.setStyleSheet(btn_blue)
        self.btn_comparar.clicked.connect(self.abrir_comparador)
        layout.addWidget(self.btn_comparar)

        self.btn_ordenar = QPushButton("Ordenar Cartas Postales")
        self.btn_ordenar.setStyleSheet(btn_blue)
        self.btn_ordenar.clicked.connect(self.ordenador_cartas)
        layout.addWidget(self.btn_ordenar)

        self.btn_generar_sgg = QPushButton("Generar SGG")
        self.btn_generar_sgg.setStyleSheet(btn_blue)
        self.btn_generar_sgg.clicked.connect(self.mostrar_en_desarrollo)
        layout.addWidget(self.btn_generar_sgg)

        self.setLayout(layout)

    def abrir_comparador(self):
        from comparador import ComparadorNombres
        self.hide()  # Oculta el menú
        self.comparador = ComparadorNombres()
        self.comparador.show()
        self.comparador.closed.connect(self.mostrar_menu)  # Al cerrar, vuelve al menú

    def ordenador_cartas(self):
        from ordenar_cartas import OrdenadorCartas
        self.hide()  # Oculta el menú
        self.ordenarCartas = OrdenadorCartas()
        self.ordenarCartas.show()
        self.ordenarCartas.closed.connect(self.mostrar_menu)  # Al cerrar, vuelve al menú

    def mostrar_menu(self):
        """ Vuelve a mostrar el menú cuando se cierra una ventana secundaria """
        self.show()

    def mostrar_en_desarrollo(self):
        QMessageBox.information(self, "En desarrollo", "Esta función aún está en desarrollo.") 
