import sys
from PySide6.QtWidgets import QApplication, QLabel

app = QApplication(sys.argv)
label = QLabel("CV Tailor works!")
label.resize(1280, 720)
label.show()
sys.exit(app.exec())