import sys
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
        self.file_path = None
        self.setStyleSheet("QMainWindow { background-color:white; }")

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

        open_action = QAction('Open', self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_drawing)
        file_menu.addAction(open_action)

        save_action = QAction('Save', self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_drawing)
        file_menu.addAction(save_action)

        save_as_action = QAction('Save As', self)
        save_as_action.setShortcut("Ctrl+Shift+S")
        save_as_action.triggered.connect(self.save_drawing_as)
        file_menu.addAction(save_as_action)

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
                painter.setPen(QPen(line[2], 12, Qt.PenStyle.SolidLine))  # Set pen width to 9 for white color
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
        self.file_path = None
        self.update()

    def open_drawing(self):
        if self.dirty:
            response = QMessageBox.question(self, "Save Changes?", "Do you want to save the current drawing?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel)
            if response == QMessageBox.StandardButton.Yes:
                self.save_drawing()
            elif response == QMessageBox.StandardButton.Cancel:
                return
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Drawing", "", "Drawing Files (*.draw)")
        if file_path:
            self.load_drawing(file_path)
            self.file_path = file_path
            self.dirty = False
            self.update()

    def save_drawing(self):
        if not self.file_path:
            self.save_drawing_as()
        else:
            self.save_drawing_to_file(self.file_path)

    def save_drawing_as(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Drawing", "", "Drawing Files (*.draw)")
        if file_path:
            self.save_drawing_to_file(file_path)
            self.file_path = file_path
            self.dirty = False

    def save_drawing_to_file(self, file_path):
        with open(file_path, 'w') as f:
            for line in self.lines:
                f.write(f"{line[0].x()},{line[0].y()},{line[1].x()},{line[1].y()},{line[2].name()}\n")
        self.update_title()

    def load_drawing(self, file_path):
        self.lines = []
        with open(file_path, 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                start = QPoint(int(parts[0]), int(parts[1]))
                end = QPoint(int(parts[2]), int(parts[3]))
                color = QColor(parts[4])
                self.lines.append((start, end, color))

    def closeEvent(self, event):
        if self.dirty:
            response = QMessageBox.question(self, "Save Changes?", "Do you want to save the current drawing?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel)
            if response == QMessageBox.StandardButton.Yes:
                self.save_drawing()
            elif response == QMessageBox.StandardButton.Cancel:
                event.ignore()
                return
        event.accept()

    def update_title(self):
        if self.file_path:
            title = f"Drawing Program - {self.file_path}"
        else:
            title = "Drawing Program"
        if self.dirty:
            title += " *"
        self.setWindowTitle(title)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    drawing_program = DrawingProgram()
    drawing_program.show()
    sys.exit(app.exec())