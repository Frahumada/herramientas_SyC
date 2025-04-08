import os
import pandas as pd
import unicodedata
import re
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QSlider, QProgressBar, QMessageBox
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from fuzzywuzzy import fuzz
from utils.estilos import btn_blue, btn_green, btn_red, progress_bar_style, ventana_principal_style
import utils.modulos as md
# from menu_principal import MenuPrincipal
def obtener_menu_principal():
    from menu_principal import MenuPrincipal
    return MenuPrincipal




class ComparadorNombres(QWidget):
    
    #funcion VOLVER MENU PRINCIPAL
    def volver_menu(self):
        self.close()  # Cierra la ventana actual
        from menu_principal import MenuPrincipal  # Importación dentro de la función para evitar importación circular
        self.menu = MenuPrincipal()  # Crea una nueva instancia del menú principal
        self.menu.show()  # Muestra el menú principal
        
    def closeEvent(self, event):
        self.closed.emit()  # Emitir la señal cuando se cierre la ventana
        event.accept()
    
    closed = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.initUI()
        self.output_folder = ""

    def initUI(self):
        self.setWindowTitle(titulo)
        self.setGeometry(100, 100, 500, 400)
        self.setStyleSheet(ventana_principal_style)

        layout = QVBoxLayout()

        self.label_archivo = QLabel("Archivo seleccionado: Ninguno")
        layout.addWidget(self.label_archivo)

        self.btn_seleccionar = QPushButton("Seleccionar Archivo")
        self.btn_seleccionar.setStyleSheet(btn_blue)
        self.btn_seleccionar.clicked.connect(self.seleccionar_archivo)
        layout.addWidget(self.btn_seleccionar)
        
        self.labelCarpeta = QLabel("Selecciona una carpeta de guardado")
        layout.addWidget(self.labelCarpeta)

        self.btnCarpeta = QPushButton("Elegir Carpeta de Guardado")
        self.btnCarpeta.setStyleSheet(btn_blue)
        self.btnCarpeta.clicked.connect(self.seleccionar_carpeta)
        layout.addWidget(self.btnCarpeta)
        

        self.slider_label = QLabel("Filtrar % Similitud (70%)")
        layout.addWidget(self.slider_label)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(70)
        self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider.setTickInterval(10)
        self.slider.valueChanged.connect(self.actualizar_slider_label)
        layout.addWidget(self.slider)

        self.btn_iniciar = QPushButton("Iniciar Comparación")
        self.btn_iniciar.setStyleSheet(btn_green)
        self.btn_iniciar.clicked.connect(self.procesar_archivo)
        layout.addWidget(self.btn_iniciar)

        self.progress = QProgressBar(self)
        layout.addWidget(self.progress)

        self.btn_volver = QPushButton("Volver al Menú Principal")
        self.btn_volver.setStyleSheet(btn_red)
        self.btn_volver.clicked.connect(self.volver_menu)
        layout.addWidget(self.btn_volver)

        self.setLayout(layout)
        self.archivo_origen = ""
    
    def seleccionar_carpeta(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta de Guardado")
        if folder_path:
            self.output_folder = folder_path
            self.labelCarpeta.setText(f"Carpeta seleccionada: {os.path.basename(folder_path)}")

    def seleccionar_archivo(self):
        archivo, _ = QFileDialog.getOpenFileName(self, "Seleccionar Archivo Excel", "", "Archivos Excel (*.xlsx *.xls)")
        if archivo:
            self.archivo_origen = archivo
            self.label_archivo.setText(f"Archivo seleccionado: {os.path.basename(archivo)}")

    def actualizar_slider_label(self, value):
        self.slider_label.setText(f"Filtrar % Similitud ({value}%)")

    def procesar_archivo(self):
        if not self.archivo_origen:
            QMessageBox.warning(self, "Error", "Por favor, selecciona un archivo primero.")
            return
        if not self.output_folder:
            QMessageBox.warning(self, "Error", "Por favor, selecciona una carpeta de destino.")
            return

        df = pd.read_excel(self.archivo_origen)

        def limpiar_texto(texto):
            if pd.isna(texto):
                return ""
            texto = str(texto).replace(",", " ")
            texto = unicodedata.normalize("NFKD", str(texto))
            texto = re.sub(r'[^a-zA-Z0-9 ]', '', texto)
            return " ".join(texto.split()).upper()

        df['TRIM(D.APYNOM)'] = df['TRIM(D.APYNOM)'].apply(limpiar_texto)
        df['TRIM(A.RESP_PAGO)'] = df['TRIM(A.RESP_PAGO)'].apply(limpiar_texto)
        df['Similitud (%)'] = df.apply(lambda x: fuzz.ratio(x['TRIM(D.APYNOM)'], x['TRIM(A.RESP_PAGO)']), axis=1)

        umbral_similitud = self.slider.value()
        df_filtrado = df[df['Similitud (%)'] >= umbral_similitud]

        carpeta_origen = os.path.dirname(self.archivo_origen)
        nombre_archivo = os.path.join(carpeta_origen, f"Resultados_{umbral_similitud}%.xlsx")
        df_filtrado.to_excel(nombre_archivo, index=False)

        QMessageBox.information(self, "Guardado", f"Archivo guardado en {nombre_archivo}")

    
