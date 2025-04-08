from utils.estilos import btn_blue, btn_green, btn_red, progress_bar_style, ventana_principal_style
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QSizePolicy, QLabel, QPushButton, QProgressBar, QHBoxLayout, QWidget
from utils.estilos import btn_blue, btn_green, btn_red
from PyQt6.QtCore import Qt

# Selector de archivo Excel
def bloque_excel(callback_excel):
    widget = QWidget()
    layout = QVBoxLayout()

    label_excel = QLabel("Selecciona un archivo Excel")
    layout.addWidget(label_excel)

    btn_excel = QPushButton("Cargar Excel")
    btn_excel.setStyleSheet(btn_blue)
    btn_excel.clicked.connect(callback_excel)
    
    # Que no se estire horizontalmente
    btn_excel.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

    # Centrar botón horizontalmente
    btn_layout = QHBoxLayout()
    btn_layout.addStretch()
    btn_layout.addWidget(btn_excel)


    layout.addLayout(btn_layout)
    widget.setLayout(layout)
    
    return widget, label_excel, btn_excel

# Selector de archivo PDF
def crear_selector_pdf(callback):
    label = QLabel("Selecciona un archivo PDF")
    boton = QPushButton("Cargar PDF")
    boton.setStyleSheet(btn_blue)
    boton.clicked.connect(callback)
    return label, boton

# Selector de carpeta
def crear_selector_carpeta(callback):
    label = QLabel("Selecciona una carpeta de guardado")
    boton = QPushButton("Elegir Carpeta de Guardado")
    boton.setStyleSheet(btn_blue)
    boton.clicked.connect(callback)
    return label, boton

# Botón de procesamiento principal
def crear_boton_procesar(callback):
    boton = QPushButton("Procesar Cartas")
    boton.setStyleSheet(btn_green)
    boton.clicked.connect(callback)
    return boton

# Botón de volver al menú principal
def crear_boton_volver(callback):
    boton = QPushButton("Volver al Menú Principal")
    boton.setStyleSheet(btn_red)
    boton.clicked.connect(callback)
    return boton

# Label + barra de progreso
def crear_barra_progreso():
    label = QLabel("Progreso:")
    barra = QProgressBar()
    return label, barra
