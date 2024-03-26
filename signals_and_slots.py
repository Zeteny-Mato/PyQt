import sys
from PyQt6.QtWidgets import QApplication, QPushButton


def function():
    print("The 'function' has been called!")

app = QApplication(sys.argv)
button = QPushButton("Call function")
button.clicked.connect(function)
button.show()
sys.exit(app.exec())