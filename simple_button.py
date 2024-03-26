import sys
from PyQt6.QtWidgets import QApplication, QPushButton

#Greetings
def say_hello():
    print("Button clicked. Hello!")

#Create the Qt Application
app = QApplication(sys.argv)

#Create a button
button = QPushButton("Click me")

#Connect the button to the function
button.clicked.connect(say_hello)

#Show the button
button.show()

#Run the main Qt loop
sys.exit(app.exec())
