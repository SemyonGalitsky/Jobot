import sys
from PySide6.QtWidgets import QApplication, QLabel

def main():
    app = QApplication(sys.argv)
    label = QLabel("CV Tailor works!")
    label.resize(1280, 720)
    label.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()