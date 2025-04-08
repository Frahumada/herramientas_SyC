import sys
from PyQt6.QtWidgets import QApplication
from menu_principal import MenuPrincipal

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MenuPrincipal()
    ventana.show()
    sys.exit(app.exec())
