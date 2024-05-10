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
        self.current_width = 3
        self.dirty = False
        self.temp_file_path = None
        self.setStyleSheet("QMainWindow { background-color:white; }")
        self.load_temp_drawing()
        self.__leftMouseButtonDown = False
        self.__startPosition = QPoint()
        self.__endPosition = QPoint()

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
        width_menu = menubar.addMenu('Width')

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

        ## Width menu actions
        width_1_action = QAction('Width 1', self)
        width_1_action.setShortcut("6")
        width_1_action.triggered.connect(lambda: self.set_width(1))
        width_menu.addAction(width_1_action)

        width_3_action = QAction('Width 3', self)
        width_3_action.setShortcut("7")
        width_3_action.triggered.connect(lambda: self.set_width(3))
        width_menu.addAction(width_3_action)

        width_5_action = QAction('Width 5', self)
        width_5_action.setShortcut("8")
        width_5_action.triggered.connect(lambda: self.set_width(5))
        width_menu.addAction(width_5_action)

        width_7_action = QAction('Width 7', self)
        width_7_action.setShortcut("9")
        width_7_action.triggered.connect(lambda: self.set_width(7))
        width_menu.addAction(width_7_action)

    def paintEvent(self, event):
        painter = QPainter(self)
        for line in self.lines:
            painter.setPen(QPen(line[2], line[3], Qt.PenStyle.SolidLine))
            painter.drawLine(line[0], line[1])

        if self.__leftMouseButtonDown:
            painter.setPen(QPen(self.current_color, self.current_width, Qt.PenStyle.SolidLine))
            painter.drawLine(self.__startPosition, self.__endPosition)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.__leftMouseButtonDown = True
            self.__startPosition = event.pos()
            self.__endPosition = event.pos()

    def mouseMoveEvent(self, event):
        if self.__leftMouseButtonDown:
            self.__endPosition = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if self.__leftMouseButtonDown:
            self.__leftMouseButtonDown = False
            self.lines.append((self.__startPosition, self.__endPosition, self.current_color, self.current_width))
            self.dirty = True

    def set_color(self, color):
        self.current_color = color

    def set_width(self, width):
        self.current_width = width

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
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Drawing", "", "Drawing Files (*.draw)")
        if file_path:
            with open(file_path, 'w') as f:
                for line in self.lines:
                    color = QColor(line[2])
                    f.write(f"{line[0].x()},{line[0].y()},{line[1].x()},{line[1].y()},{color.name()},{line[3]}\n")
            self.dirty = False
            self.temp_file_path = file_path

    def load_temp_drawing(self):
        if self.temp_file_path and os.path.exists(self.temp_file_path):
            with open(self.temp_file_path, 'r') as f:
                self.lines = []
                for line in f:
                    parts = line.strip().split(',')
                    start = QPoint(int(parts[0]), int(parts[1]))
                    end = QPoint(int(parts[2]), int(parts[3]))
                    color = QColor(parts[4])
                    width = int(parts[5])
                    self.lines.append((start, end, color, width))
            self.update()
    
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    drawing_program = DrawingProgram()
    drawing_program.show()
    sys.exit(app.exec())