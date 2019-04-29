import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout,
                            QHBoxLayout, QPushButton)
from PyQt5.QtCore import pyqtSlot
from paint import drawing_window

class Window(QWidget):
    def __init__(self):
        super().__init__()

        #Window Title
        self.setWindowTitle("Home Page")

        #Welcome Message
        self.welcome = QLabel("Welcome!!\nClick on the button below to access the app.")
        

        #Button that takes you to the app.
        self.app_button = QPushButton("Start Drawing!!")
        self.clear_screen = QPushButton("Clear the Canvas")
        self.app_button.clicked.connect(self.on_click)
        self.clear_screen.clicked.connect(self.on_click)


        #Window Setup
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.welcome)
        self.vbox.addWidget(self.app_button)
        self.vbox.addWidget(self.clear_screen)
        self.setLayout(self.vbox)

    @pyqtSlot()
    def on_click(self):
        drawing_window()

app = QApplication(sys.argv)
main = Window()
main.show()
sys.exit(app.exec_())
