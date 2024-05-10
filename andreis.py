# Import necessary modules from PyQt6
from PyQt6 import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

# Define the main window class


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the size and title of the window
        self.setFixedSize(800, 600)
        self.setWindowTitle("Drawing App")

        # Initialize drawing variables
        self.previousPoint = None
        self.drawing = False
        self.drawingLine = False
        self.lineStart = QPoint()
        self.tempCanvas = None

        # Create a QLabel to hold the canvas QPixmap
        self.label = QLabel()

        # Create a QPixmap for the canvas and fill it with white
        self.canvas = QPixmap(QSize(800, 600))
        self.canvas.fill(QColor("white"))

        # Create a QPen for drawing on the canvas
        self.pen = QPen()
        self.pen.setWidth(6)
        self.pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        # Set the QPixmap as the pixmap of the QLabel
        self.label.setPixmap(self.canvas)
        # Set the QLabel as the central widget of the QMainWindow
        self.setCentralWidget(self.label)

        # Create a toolbar
        toolbar = QToolBar("Toolbar")
        toolbar.setMovable(False)

        # Create actions for the toolbar
        colorAction = QAction("Choose Color", self)
        colorAction.triggered.connect(self.changeColor)
        toolbar.addAction(colorAction)

        # Create a menu for brush sizes
        brushSizeMenu = QMenu("Brush Size", self)
        for size in [2, 4, 6, 8, 10]:
            sizeAction = QAction(str(size), self)
            sizeAction.triggered.connect(
                lambda checked, s=size: self.changeBrushSize(s))
            brushSizeMenu.addAction(sizeAction)

        # Create a tool button for the brush size menu
        brushSizeButton = QToolButton(self)
        brushSizeButton.setMenu(brushSizeMenu)
        brushSizeButton.setPopupMode(
            QToolButton.ToolButtonPopupMode.InstantPopup)
        brushSizeButton.setText("Brush Size")
        toolbar.addWidget(brushSizeButton)

        # More actions for the toolbar
        eraserAction = QAction("Eraser", self)
        eraserAction.triggered.connect(self.useEraser)
        toolbar.addAction(eraserAction)

        clearAction = QAction("Clear Canvas", self)
        clearAction.triggered.connect(self.clearCanvas)
        toolbar.addAction(clearAction)

        saveAction = QAction("Save", self)
        saveAction.triggered.connect(self.saveToFile)
        toolbar.addAction(saveAction)

        # Add the toolbar to the QMainWindow
        self.addToolBar(toolbar)

    # Method to save the canvas to a file
    def saveToFile(self):
        dialog = QFileDialog()
        dialog.setNameFilter("*.jpg")
        dialog.setDefaultSuffix(".jpg")
        clickedOk = dialog.exec()

        if clickedOk:
            self.canvas.save(dialog.selectedFiles()[0])

    # Method to change the color of the pen
    def changeColor(self):
        dialog = QColorDialog()
        clickedOk = dialog.exec()

        if clickedOk:
            self.pen.setColor(dialog.currentColor())

    # Method to clear the canvas
    def clearCanvas(self):
        self.canvas.fill(QColor("white"))
        self.label.setPixmap(self.canvas)

    # Method to use the eraser
    def useEraser(self):
        self.pen.setColor(QColor("white"))

    # Method to change the brush size
    def changeBrushSize(self, size):
        self.pen.setWidth(size)

    # Event handler for mouse press events
    def mousePressEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.drawing = True
            self.previousPoint = event.pos()
            self.previousPoint.setY(self.previousPoint.y() - 20)
        elif event.buttons() == Qt.MouseButton.RightButton:
            self.drawingLine = True
            self.lineStart = event.pos()
            self.lineStart.setY(self.lineStart.y() - 20)

    # Event handler for mouse move events
    def mouseMoveEvent(self, event):
        position = event.pos()
        position.setY(position.y() - 20)

        if self.previousPoint and self.drawing:
            painter = QPainter(self.canvas)
            painter.setPen(self.pen)
            painter.drawLine(self.previousPoint.x(),
                             self.previousPoint.y(), position.x(), position.y())
            self.previousPoint = position
            painter.end()
        elif self.drawingLine:
            if self.tempCanvas:
                self.canvas = self.tempCanvas.copy()
            else:
                self.tempCanvas = self.canvas.copy()
            tempPainter = QPainter(self.canvas)
            tempPainter.setPen(self.pen)
            tempPainter.drawLine(self.lineStart, position)
            tempPainter.end()
            self.update()

        self.label.setPixmap(self.canvas)

    # Event handler for mouse release events
    def mouseReleaseEvent(self, event):
        if self.drawingLine:
            position = event.pos()
            position.setY(position.y() - 20)

            painter = QPainter(self.canvas)
            painter.setPen(self.pen)
            painter.drawLine(self.lineStart, position)
            painter.end()
            self.label.setPixmap(self.canvas)
            self.tempCanvas = None

        self.drawing = False
        self.drawingLine = False


# Create a QApplication
app = QApplication([])
# Create an instance of the MainWindow
window = MainWindow()
# Show the MainWindow
window.show()
# Start the QApplication event loop
app.exec()