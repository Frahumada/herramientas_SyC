# utils/estilos.py

# === Botones ===
btn_blue = """
QPushButton {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                      stop:0 #ededed, stop:1 #dfdfdf);
    border-radius: 6px;
    border: 1px solid #dcdcdc;
    color: #777777;
    font-family: Arial;
    font-size: 15px;
    font-weight: bold;
    padding: 6px 24px;
    text-align: center;
}
QPushButton:hover {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                      stop:0 #dfdfdf, stop:1 #ededed);
}
QPushButton:pressed {
    padding-top: 7px;
    padding-bottom: 5px;
}
"""

btn_green = """
QPushButton {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                      stop:0 #9fdf9f, stop:1 #4CAF50);
    border-radius: 6px;
    border: 1px solid #3c9a3c;
    color: white;
    font-family: Arial;
    font-size: 15px;
    font-weight: bold;
    padding: 6px 24px;
    text-align: center;
}
QPushButton:hover {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                      stop:0 #4CAF50, stop:1 #9fdf9f);
}
QPushButton:pressed {
    padding-top: 7px;
    padding-bottom: 5px;
}
"""

btn_red = """
QPushButton {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                      stop:0 #f66, stop:1 #d33);
    border-radius: 6px;
    border: 1px solid #aa2222;
    color: white;
    font-family: Arial;
    font-size: 15px;
    font-weight: bold;
    padding: 6px 24px;
    text-align: center;
}
QPushButton:hover {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                      stop:0 #d33, stop:1 #f66);
}
QPushButton:pressed {
    padding-top: 7px;
    padding-bottom: 5px;
}
"""
# === Barra de Progreso ===
progress_bar_style = """
QProgressBar {
    border: 1px solid #bbb;
    border-radius: 5px;
    text-align: center;
    background-color: #eee;
}
QProgressBar::chunk {
    background-color: #4CAF50;
    width: 20px;
}
"""

# === Estilo general del widget ===
ventana_principal_style = """
QWidget {
    background-color: #f5f5f5;
    font-family: 'Segoe UI';
    font-size: 12pt;
}
QLabel {
    color: #333;
    font-weight: bold;
}
"""
