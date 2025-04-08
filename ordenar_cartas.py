import os
import sys
import pandas as pd
import fitz  # PyMuPDF
import re
from PyQt6.QtWidgets import (
    QProgressBar,
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QFileDialog,
    QLabel,
)
from PyQt6.QtCore import pyqtSignal
from utils.estilos import (
    btn_blue,
    btn_green,
    btn_red,
    progress_bar_style,
    ventana_principal_style,
)
from utils.modulos import (
    bloque_excel,
    crear_selector_pdf,
    crear_selector_carpeta,
    crear_boton_procesar,
    crear_boton_volver,
    crear_barra_progreso,
)


class OrdenadorCartas(QWidget):
    def closeEvent(self, event):
        self.closed.emit()  # Emitir la señal cuando se cierre la ventana
        event.accept()

    closed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()
        self.excel_path = ""
        self.pdf_path = ""
        self.output_folder = ""

    def volver_menu(self):
        self.close()  # Cierra la ventana actual
        from menu_principal import (
            MenuPrincipal,
        )  # Importación dentro de la función para evitar importación circular

        self.menu = MenuPrincipal()  # Crea una nueva instancia del menú principal
        self.menu.show()  # Muestra el menú principal

    def initUI(self):
        layout = QVBoxLayout()
        self.setStyleSheet(ventana_principal_style)

        # Modulo seleccion excel
        excel_widget, self.labelExcel, self.btnExcel = bloque_excel(self.cargar_excel)
        layout.addWidget(excel_widget)
        layout.setStretch(0, 3)
        layout.setStretch(1, 1)

        # Modulo seleccion PDF
        self.labelPDF, self.btnPDF = crear_selector_pdf(self.cargar_pdf)
        layout.addWidget(self.labelPDF)
        layout.addWidget(self.btnPDF)

        # Modulo seleccion carpeta destino
        self.labelCarpeta, self.btnCarpeta = crear_selector_carpeta(
            self.seleccionar_carpeta
        )
        layout.addWidget(self.labelCarpeta)
        layout.addWidget(self.btnCarpeta)

        # Modulo boton procesar
        self.btnProcesar = crear_boton_procesar(self.procesar_cartas)
        layout.addWidget(self.btnProcesar)

        # Modulo boton volver al menu principal
        self.btn_volver = crear_boton_volver(self.volver_menu)
        layout.addWidget(self.btn_volver)

        # Modulo progreso
        self.progreso_label, self.progress_bar = crear_barra_progreso()
        layout.addWidget(self.progreso_label)
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)
        self.setWindowTitle("Distribuir Cartas Postales")

    def seleccionar_carpeta(self):
        folder_path = QFileDialog.getExistingDirectory(
            self, "Seleccionar Carpeta de Guardado"
        )
        if folder_path:
            self.output_folder = folder_path
            self.labelCarpeta.setText(
                f"Carpeta seleccionada: {os.path.basename(folder_path)}"
            )

    def cargar_excel(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar Archivo Excel", "", "Archivos Excel (*.xlsx *.xls)"
        )
        if file_path:
            self.excel_path = file_path
            self.labelExcel.setText(
                f"Archivo seleccionado: {os.path.basename(file_path)}"
            )

    def cargar_pdf(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar Archivo PDF", "", "Archivos PDF (*.pdf)"
        )
        if file_path:
            self.pdf_path = file_path
            self.labelPDF.setText(
                f"Archivo seleccionado: {os.path.basename(file_path)}"
            )

    def limpiar_texto(self, texto):
        texto = texto.strip().replace("\n", " ")
        return re.sub(" +", " ", texto)

    def buscar_partida_en_texto(self, texto, partidas_barrio):
        texto_limpio = self.limpiar_texto(texto)
        for partida, barrio in partidas_barrio:
            if f": {partida} " in texto_limpio:
                return partida, barrio
        return None, None

    def procesar_cartas(self):
        if not self.excel_path or not self.pdf_path:
            print("Debes seleccionar un archivo Excel y un PDF.")
            return
        if not self.output_folder:
            print("Debes seleccionar una carpeta de guardado.")
            return

        df = pd.read_excel(self.excel_path, header=0)

        # Depuración para ver las columnas y las primeras filas
        print("Columnas del archivo Excel:", df.columns)
        print("Primeras filas del archivo Excel:", df.head())

        # Limpiar los nombres de las columnas
        df.columns = df.columns.str.strip().str.lower()

        # Verificar si los nombres de las columnas son correctos
        print("Columnas después de la limpieza:", df.columns)

        # Ahora puedes acceder a las columnas correctamente
        df["partida"] = df["partida"].astype(str).str.strip()
        df["barrio"] = df["barrio"].astype(str).str.strip()
        partidas_barrio = list(zip(df["partida"], df["barrio"]))

        documento = fitz.open(self.pdf_path)
        paginas_por_barrio = {}

        omitir = set(
            [
                "223805",
                "223806",
                "223807",
                "223820",
                "223835",
                "223837",
                "223845",
                "223885",
                "223926",
                "223959",
                "223965",
                "223989",
            ]
        )

        for i in range(len(documento)):
            pagina = documento.load_page(i)
            texto_pagina = pagina.get_text()

            if texto_pagina:
                partida, barrio = self.buscar_partida_en_texto(
                    texto_pagina, partidas_barrio
                )

                # Verifica que la partida no esté en la lista de omitir
                if partida and partida not in omitir:
                    # Verifica que también haya un barrio identificado
                    if barrio:
                        if barrio not in paginas_por_barrio:
                            paginas_por_barrio[barrio] = []
                        paginas_por_barrio[barrio].append(pagina)

        total = len(paginas_por_barrio)
        self.progress_bar.setMaximum(total)
        self.progress_bar.setValue(0)

        for index, (barrio, paginas) in enumerate(paginas_por_barrio.items(), start=1):
            self.progreso_label.setText(f"Procesando barrio: {barrio}")
            nuevo_documento = fitz.open()
            for pagina in paginas:
                nuevo_documento.insert_pdf(
                    documento, from_page=pagina.number, to_page=pagina.number
                )
            nombre_archivo = f"cartas_{barrio}.pdf"
            nuevo_documento.save(nombre_archivo, garbage=4)
            nuevo_documento.close()
            print(f"Archivo guardado: {nombre_archivo} - {len(paginas)} Paginas")

            # Actualizar progreso
            self.progress_bar.setValue(index)
            QApplication.processEvents()  # Para que se actualice visualmente

        documento.close()
        print("Proceso finalizado.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = OrdenadorCartas()
    ventana.show()
    sys.exit(app.exec())
