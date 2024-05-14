from PyQt6 import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set fixed size and window title
        self.setFixedSize(800, 600)
        self.setWindowTitle("Drawing App")

        # Variables to manage drawing state
        self.previousPoint = None
        self.drawing = False
        self.drawingLine = False
        self.lineStart = QPoint()
        self.tempCanvas = None

        # Create a white canvas using QPixmap
        self.label = QLabel()
        self.canvas = QPixmap(QSize(800, 600))
        self.canvas.fill(QColor("white"))

        # Set canvas as the pixmap for the label
        self.label.setPixmap(self.canvas)
        self.setCentralWidget(self.label)

        # Initialize drawing properties
        self.pen = QPen()
        self.pen.setWidth(6)
        self.pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        # Menu and actions setup
        self.currentFileName = None
        self.dirty = False
        self.updateWindowTitle()

        # Create toolbar
        toolbar = QToolBar("Toolbar")
        toolbar.setMovable(False)

        # File menu actions
        fileMenu = QMenu("File", self)

        saveAction = QAction("Save", self)
        saveAction.triggered.connect(self.saveToFile)
        fileMenu.addAction(saveAction)

        saveAsAction = QAction("Save As", self)
        saveAsAction.triggered.connect(lambda: self.saveAsToFile())
        fileMenu.addAction(saveAsAction)

        openAction = QAction("Open", self)
        openAction.triggered.connect(self.openFile)
        fileMenu.addAction(openAction)

        newAction = QAction("New", self)
        newAction.triggered.connect(self.newFile)
        fileMenu.addAction(newAction)

        # File menu button on the toolbar
        fileButton = QToolButton(self)
        fileButton.setMenu(fileMenu)
        fileButton.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        fileButton.setText("File")
        toolbar.addWidget(fileButton)

        # Color selection action
        colorAction = QAction("Choose Color", self)
        colorAction.triggered.connect(self.changeColor)
        toolbar.addAction(colorAction)

        # Brush size selection
        brushSizeMenu = QMenu("Brush Size", self)
        for size in [2, 4, 6, 8, 10]:
            sizeAction = QAction(str(size), self)
            sizeAction.triggered.connect(
                lambda checked, s=size: self.changeBrushSize(s))
            brushSizeMenu.addAction(sizeAction)

        brushSizeButton = QToolButton(self)
        brushSizeButton.setMenu(brushSizeMenu)
        brushSizeButton.setPopupMode(
            QToolButton.ToolButtonPopupMode.InstantPopup)
        brushSizeButton.setText("Brush Size")
        toolbar.addWidget(brushSizeButton)

        # Eraser action
        eraserAction = QAction("Eraser", self)
        eraserAction.triggered.connect(self.useEraser)
        toolbar.addAction(eraserAction)

        # Clear canvas action
        clearAction = QAction("Clear Canvas", self)
        clearAction.triggered.connect(self.clearCanvas)
        toolbar.addAction(clearAction)

        # Add toolbar to the main window
        self.addToolBar(toolbar)

    def updateWindowTitle(self):
        # Update window title based on file name and dirty state
        title = "Drawing App"
        if self.currentFileName:
            title += " - " + self.currentFileName
        if self.dirty:
            title += "*"
        super().setWindowTitle(title)

    def saveToFile(self):
        # Save canvas to a file
        if self.currentFileName:
            self.canvas.save(self.currentFileName)
            self.dirty = False
            self.setWindowTitle(f"Drawing App - {self.currentFileName}")
        else:
            self.saveAsToFile()

    def saveAsToFile(self):
        # Save canvas to a new file
        fileName, _ = QFileDialog.getSaveFileName(
            self, "Save As", "", "JPEG (*.jpg);;All Files (*)")
        if fileName:
            self.canvas.save(fileName)
            self.currentFileName = fileName
            self.dirty = False
            self.setWindowTitle(f"Drawing App - {self.currentFileName}")

    def openFile(self):
        # Open an image file
        fileName, _ = QFileDialog.getOpenFileName(
            self, "QFileDialog.getOpenFileName()", "", "Images (*.png *.xpm *.jpg)")
        if fileName:
            self.canvas.load(fileName)
            self.label.setPixmap(self.canvas)
            self.currentFileName = fileName
            self.dirty = False
            self.setWindowTitle(f"Drawing App - {self.currentFileName}")

    def newFile(self):
        # Create a new blank canvas
        self.canvas.fill(QColor("white"))
        self.label.setPixmap(self.canvas)
        self.currentFileName = None
        self.dirty = False

    def changeColor(self):
        # Change drawing color using QColorDialog
        dialog = QColorDialog()
        clickedOk = dialog.exec()

        if clickedOk:
            self.pen.setColor(dialog.currentColor())

    def clearCanvas(self):
        # Clear the canvas
        self.canvas.fill(QColor("white"))
        self.label.setPixmap(self.canvas)
        self.dirty = True
        self.updateWindowTitle()

    def useEraser(self):
        # Set pen color to white for erasing
        self.pen.setColor(QColor("white"))

    def changeBrushSize(self, size):
        # Change pen width for drawing
        self.pen.setWidth(size)

    def mousePressEvent(self, event):
        # Handle mouse press events
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.drawing = True
            self.previousPoint = event.pos()
            self.previousPoint.setY(self.previousPoint.y() - 20)
        elif event.buttons() == Qt.MouseButton.RightButton:
            self.drawingLine = True
            self.lineStart = event.pos()
            self.lineStart.setY(self.lineStart.y() - 20)

    def mouseMoveEvent(self, event):
        # Handle mouse move events for drawing
        position = event.pos()
        position.setY(position.y() - 20)

        if self.previousPoint and self.drawing:
            painter = QPainter(self.canvas)
            painter.setPen(self.pen)
            painter.drawLine(self.previousPoint.x(),
                             self.previousPoint.y(), position.x(), position.y())
            self.previousPoint = position
            painter.end()
            self.dirty = True
            self.updateWindowTitle()
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

    def mouseReleaseEvent(self, event):
        # Handle mouse release events
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

    def closeEvent(self, event: QCloseEvent) -> None:
        # Override close event to handle unsaved changes
        if self.dirty:
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Exit")
            msg_box.setWindowIcon(self.windowIcon())
            msg_box.setIcon(QMessageBox.Icon.Information)
            msg_box.setText(
                "You have unsaved changes. Do you want to save your changes?")
            msg_box.setStandardButtons(
                QMessageBox.StandardButton.Yes |
                QMessageBox.StandardButton.No |
                QMessageBox.StandardButton.Cancel)

            return_value: QMessageBox.StandardButton = msg_box.exec()
            if return_value == QMessageBox.StandardButton.Yes:
                self.saveToFile()
                event.accept()
            elif return_value == QMessageBox.StandardButton.No:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()


# Create and run the application
app = QApplication([])
window = MainWindow()
window.show()
app.exec()