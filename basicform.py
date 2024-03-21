import sys
from PyQt6.QtWidgets import QWidget, QLabel, QApplication

class BasicForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setupGUI()
    
    def setupGUI(self):
        #pass
        self.label = QLabel("Hello World!")
        self.label.setParent(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    form = BasicForm()
    form.show()

    app.exec()