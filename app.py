

import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout,
                            QHBoxLayout, QPushButton, QComboBox)
from PyQt5.QtCore import pyqtSlot
from paint import DrawingWindow
import numpy as np
import cv2
import speech as VoiceRecord
from collections import deque

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.our_window = DrawingWindow()
        self.voiceObject = VoiceRecord.VoiceRecord();

        #Window Title
        self.setWindowTitle("Home Page")

        #Welcome Message
        self.welcome = QLabel("Welcome!!\nClick on the button below to access the app.")
        self.color_message = QLabel("Change the color of the line.")
        self.delete_message = QLabel("Clear the canvas.")


        #Button that takes you to the app.
        self.app_button = QPushButton("Start Drawing!!")
        self.app_button.clicked.connect(self.on_click)

        #Button that clears canvas
        self.delete_button = QPushButton("Erase Everything")
        self.delete_button.clicked.connect(self.clear_canvas)

        #Button to listen for voice commands
        self.voice_button = QPushButton("Voice Command")
        self.voice_button.clicked.connect(self.voice_click)


        #Colors Combobox
        options = ["blue", "green", "red", "yellow"]
        self.choose_color = QComboBox()
        self.choose_color.addItems(options)
        self.choose_color.currentIndexChanged.connect(self.color_chosen)


        #Window Setup
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.welcome)
        self.vbox.addWidget(self.app_button)
        self.vbox.addWidget(self.delete_message)
        self.vbox.addWidget(self.delete_button)
        self.vbox.addWidget(self.color_message)
        self.vbox.addWidget(self.choose_color)
        self.vbox.addWidget(self.voice_button)
        self.setLayout(self.vbox)

    @pyqtSlot()
    def on_click(self):
        print("Clicked!!")
        self.our_window.clear_everything()
        self.our_window.paintWindow = np.zeros((471,636,3)) + 255
        self.our_window.camera = cv2.VideoCapture(0)
        self.our_window.draw()


    def voice_click(self):
        print("Voice Clicked!!")
        text = self.voiceObject.send_text();

        print(text)

        if text.lower() == "change color to blue":
            self.our_window.colorIndex = 0;
        elif text.lower() == "change color to green":
            self.our_window.colorIndex = 1;
        elif text.lower() == "change color to red":
            self.our_window.colorIndex = 2;
        elif text.lower() == "change color to yellow":
            self.our_window.colorIndex = 3;
        elif text.lower() == "erase everything":
            self.our_window.clear_everything()


    def color_chosen(self):
        new_color = self.choose_color.currentText()
        if(new_color == "blue"):
            self.our_window.colorIndex = 0
        elif new_color == 'green':
            self.our_window.colorIndex = 1
        elif new_color == 'red':
            self.our_window.colorIndex = 2
        else:
            self.our_window.colorIndex = 3

    def clear_canvas(self):
        self.our_window.clear_everything()


app = QApplication(sys.argv)
main = Window()
main.show()
sys.exit(app.exec_())
