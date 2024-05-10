import sys
import os
import tempfile
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QWidget, QVBoxLayout, QToolBar, QColorDialog, QMenu, QToolButton
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
        self.free_draw_mode = False

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

        ## Create toolbar
        toolbar = QToolBar("Toolbar")
        self.addToolBar(toolbar)

        ## Window actions menu
        window_actions_menu = QMenu("Window Actions", self)
        new_action = QAction("New", self)
        new_action.triggered.connect(self.new_drawing)
        window_actions_menu.addAction(new_action)
        open_action = QAction("Open", self)
        open_action.triggered.connect(self.open_drawing)
        window_actions_menu.addAction(open_action)
        save_action = QAction("Save", self)
        save_action.triggered.connect(self.save_drawing)
        window_actions_menu.addAction(save_action)
        save_as_action = QAction("Save As", self)
        save_as_action.triggered.connect(self.save_drawing_as)
        window_actions_menu.addAction(save_as_action)
        close_action = QAction("Close", self)
        close_action.triggered.connect(self.close)
        window_actions_menu.addAction(close_action)

        ## Window actions button
        window_actions_button = QToolButton(self)
        window_actions_button.setMenu(window_actions_menu)
        window_actions_button.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        window_actions_button.setText("Window Actions")
        toolbar.addWidget(window_actions_button)

        ## Color menu
        color_menu = QMenu("Color", self)
        black_action = QAction("Black", self)
        black_action.triggered.connect(lambda: self.set_color(Qt.GlobalColor.black))
        color_menu.addAction(black_action)
        red_action = QAction("Red", self)
        red_action.triggered.connect(lambda: self.set_color(Qt.GlobalColor.red))
        color_menu.addAction(red_action)
        green_action = QAction("Green", self)
        green_action.triggered.connect(lambda: self.set_color(Qt.GlobalColor.green))
        color_menu.addAction(green_action)
        blue_action = QAction("Blue", self)
        blue_action.triggered.connect(lambda: self.set_color(Qt.GlobalColor.blue))
        color_menu.addAction(blue_action)
        white_action = QAction("Eraser", self)
        white_action.triggered.connect(lambda: self.set_color(Qt.GlobalColor.white))
        color_menu.addAction(white_action)

        ## Color button
        color_button = QToolButton(self)
        color_button.setMenu(color_menu)
        color_button.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        color_button.setText("Color")
        toolbar.addWidget(color_button)

        ## Brush size menu
        brush_size_menu = QMenu("Brush Size", self)
        width_1_action = QAction("Width 1 pixel", self)
        width_1_action.triggered.connect(lambda: self.set_width(1))
        brush_size_menu.addAction(width_1_action)
        width_3_action = QAction("Width: 3 pixels", self)
        width_3_action.triggered.connect(lambda: self.set_width(3))
        brush_size_menu.addAction(width_3_action)
        width_5_action = QAction("Width: 5 pixels", self)
        width_5_action.triggered.connect(lambda: self.set_width(5))
        brush_size_menu.addAction(width_5_action)
        width_7_action = QAction("Width: 10 pixels", self)
        width_7_action.triggered.connect(lambda: self.set_width(10))
        brush_size_menu.addAction(width_7_action)

        ## Brush size button
        brush_size_button = QToolButton(self)
        brush_size_button.setMenu(brush_size_menu)
        brush_size_button.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        brush_size_button.setText("Brush Size")
        toolbar.addWidget(brush_size_button)

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
            if self.current_color == Qt.GlobalColor.white:
                self.free_draw_mode = True

    def mouseMoveEvent(self, event):
        if self.__leftMouseButtonDown:
            self.__endPosition = event.pos()
            if self.current_color == Qt.GlobalColor.white and self.free_draw_mode:
                self.lines.append((self.__startPosition, self.__endPosition, self.current_color, self.current_width))
                self.__startPosition = self.__endPosition
            self.update()

    def mouseReleaseEvent(self, event):
        if self.__leftMouseButtonDown:
            self.__leftMouseButtonDown = False
            if not (self.current_color == Qt.GlobalColor.white and self.free_draw_mode):
                self.lines.append((self.__startPosition, self.__endPosition, self.current_color, self.current_width))
            self.dirty = True
            self.free_draw_mode = False

    def change_color(self):
        color_dialog = QColorDialog(self)
        if color_dialog.exec():
            self.current_color = color_dialog.selectedColor()

    def change_width(self, width):
        self.current_width = width

    def use_eraser(self):
        self.pen.setColor(QColor("white"))

    def clear_canvas(self):
        self.canvas.fill(QColor("white"))
        self.label.setPixmap(self.canvas)

    def save_drawing(self):
        if not self.temp_file_path:
            self.save_drawing_as()
        else:
            self.save_drawing_to_file(self.temp_file_path)

    def save_drawing_as(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Drawing", "", "Drawing Files (*.draw)")
        if file_path:
            with open(file_path, 'w') as f:
                for line in self.lines:
                    color = QColor(line[2])
                    f.write(f"{line[0].x()},{line[0].y()},{line[1].x()},{line[1].y()},{color.name()}\n")
            self.save_drawing_to_file(file_path)
            self.temp_file_path = file_path
            self.dirty = False

    def save_drawing_to_file(self, file_path):
        with open(file_path, 'w') as f:
            for line in self.lines:
                color = QColor(line[2])
                f.write(f"{line[0].x()},{line[0].y()},{line[1].x()},{line[1].y()},{color.name()},{line[3]}\n")

    def set_color(self, color):
        self.current_color = color

    def set_width(self, width):
        self.current_width = width

    def new_drawing(self):
        if self.dirty:
            response = QMessageBox.question(self, "Save Changes?", "Do you want to save the current drawing?",
                                            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel)
            if response == QMessageBox.StandardButton.Yes:
                self.save_drawing()
            elif response == QMessageBox.StandardButton.Cancel:
                return
        self.lines = []
        self.dirty = False
        self.temp_file_path = None
        self.canvas.fill(QColor("white"))
        self.label.setPixmap(self.canvas)
        self.update()

    def open_drawing(self):
        if self.dirty:
            response = QMessageBox.question(self, "Save Changes?", "Do you want to save the current drawing?",
                                            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel)
            if response == QMessageBox.StandardButton.Yes:
                self.save_drawing()
            elif response == QMessageBox.StandardButton.Cancel:
                return
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Drawing", "", "Drawing Files (*.draw)")
        if file_path:
            self.load_drawing(file_path)
            self.temp_file_path = file_path
            self.dirty = False
            self.update()

    def load_drawing(self, file_path):
        with open(file_path, 'r') as f:
            self.lines = []
            for line in f:
                parts = line.strip().split(',')
                start = QPoint(int(parts[0]), int(parts[1]))
                end = QPoint(int(parts[2]), int(parts[3]))
                color = QColor(parts[4])
                width = int(parts[5])
                self.lines.append((start, end, color, width))
        self.canvas.fill(QColor("white"))
        self.update()

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

    def closeEvent(self, event):
        if self.dirty:
            response = QMessageBox.question(self, "Save Changes?", "Do you want to save the current drawing?",
                                            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel)
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