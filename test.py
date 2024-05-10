import sys
import os
import tempfile
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QWidget, QVBoxLayout
from PyQt6.QtGui import QPainter, QPen, QColor, QAction
from PyQt6.QtCore import Qt, QPoint

class DrawingProgram(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.lines = []
        self.current_color = Qt.GlobalColor.black
        self.dirty = False
        self.temp_file_path = None
        self.setStyleSheet("QMainWindow { background-color:white; }")
        self.load_temp_drawing()

    def initUI(self):
        ## Window setup
        self.setWindowTitle("Drawing Program")
        self.setGeometry(100, 100, 800, 600)

        ## Create central widget and layout
        central_widget = QWidget()
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        ## Create menu bar
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')
        color_menu = menubar.addMenu('Color')

        ## File menu actions
        new_action = QAction('New', self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_drawing)
        file_menu.addAction(new_action)

        save_action = QAction('Save', self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_drawing)
        file_menu.addAction(save_action)

        exit_action = QAction('Close', self)
        exit_action.setShortcut("Ctrl+W")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        ## Color menu actions
        black_action = QAction('Black', self)
        black_action.setShortcut("1")
        black_action.triggered.connect(lambda: self.set_color(Qt.GlobalColor.black))
        color_menu.addAction(black_action)

        red_action = QAction('Red', self)
        red_action.setShortcut("2")
        red_action.triggered.connect(lambda: self.set_color(Qt.GlobalColor.red))
        color_menu.addAction(red_action)

        green_action = QAction('Green', self)
        green_action.setShortcut("3")
        green_action.triggered.connect(lambda: self.set_color(Qt.GlobalColor.green))
        color_menu.addAction(green_action)

        blue_action = QAction('Blue', self)
        blue_action.setShortcut("4")
        blue_action.triggered.connect(lambda: self.set_color(Qt.GlobalColor.blue))
        color_menu.addAction(blue_action)

        white_action = QAction('Eraser', self)
        white_action.setShortcut("5")
        white_action.triggered.connect(lambda: self.set_color(Qt.GlobalColor.white))
        color_menu.addAction(white_action)

    def paintEvent(self, event):
        painter = QPainter(self)
        for line in self.lines:
            if line[2] == Qt.GlobalColor.white:
                painter.setPen(QPen(line[2], 9, Qt.PenStyle.SolidLine))  # Set pen width to 9 for white color
            else:
                painter.setPen(QPen(line[2], 3, Qt.PenStyle.SolidLine))  # Set pen width to 3 for other colors
            painter.drawLine(line[0], line[1])

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.last_point = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            new_point = event.pos()
            self.lines.append((self.last_point, new_point, self.current_color))
            self.last_point = new_point
            self.update()
            self.dirty = True

    def set_color(self, color):
        self.current_color = color

    def new_drawing(self):
        if self.dirty:
            response = QMessageBox.question(self, "Save Changes?", "Do you want to save the current drawing?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel)
            if response == QMessageBox.StandardButton.Yes:
                self.save_drawing()
            elif response == QMessageBox.StandardButton.Cancel:
                return
        self.lines = []
        self.dirty = False
        self.temp_file_path = None
        self.update()

    def save_drawing(self):
    # Create a dialog to get the file path from the user
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Drawing", "", "Drawing Files (*.draw)")
    
    # If the user didn't cancel the dialog
        if file_path:
            with open(file_path, 'w') as f:
                for line in self.lines:
                    color = QColor(line[2])  # Convert Qt.GlobalColor to QColor
                    f.write(f"{line[0].x()},{line[0].y()},{line[1].x()},{line[1].y()},{color.name()}\n")
            self.dirty = False
            self.temp_file_path = file_path  # Store the file path for future use


    def load_temp_drawing(self):
        if self.temp_file_path and os.path.exists(self.temp_file_path):
            with open(self.temp_file_path, 'r') as f:
                self.lines = []
                for line in f:
                    parts = line.strip().split(',')
                    start = QPoint(int(parts[0]), int(parts[1]))
                    end = QPoint(int(parts[2]), int(parts[3]))
                    color = QColor(parts[4])
                    self.lines.append((start, end, color))
        self.update()


    def closeEvent(self, event):
        if self.dirty:
            response = QMessageBox.question(self, "Save Changes?", "Do you want to save the current drawing?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel)
            if response == QMessageBox.StandardButton.Yes:
                self.save_drawing()
            elif response == QMessageBox.StandardButton.Cancel:
                event.ignore()
                return
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    drawing_program = DrawingProgram()
    drawing_program.show()
    sys.exit(app.exec())
