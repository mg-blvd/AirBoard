import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout,
                            QHBoxLayout, QPushButton, QComboBox, QLineEdit)
from PyQt5.QtCore import pyqtSlot
from paint import DrawingWindow
import numpy as np
import cv2
import speech as VoiceRecord
from collections import deque


from pygame import mixer # Load the required library




class Window(QWidget):
    def __init__(self):
        super().__init__()
        mixer.init()

        self.our_window = DrawingWindow()
        self.voiceObject = VoiceRecord.VoiceRecord();

        #Window Title
        self.setWindowTitle("Home Page")

        #Welcome Message
        self.welcome = QLabel("Welcome!!\nClick on the button below to access the app.")
        self.color_message = QLabel("Change the color of the line.")


        #Button that takes you to the app.
        self.app_button = QPushButton("Start Drawing!!")
        self.app_button.clicked.connect(self.on_click)

        #Button that deleates clear_everything
        self.clear_button = QPushButton("Clear the Screen")
        self.clear_button.clicked.connect(self.clean_screen)


        #Button to listen for voice commands
        self.voice_button = QPushButton("Voice Command")
        self.voice_button.clicked.connect(self.voice_click)

        #Button to listen for save
        self.save_button1 = QPushButton("Save drawing")
        self.save_button1.clicked.connect(self.save_image1)
        self.save_button2 = QPushButton("Save drawing with background")
        self.save_button2.clicked.connect(self.save_image2)


        #Colors Combobox
        options = ["blue", "green", "red", "yellow"]
        self.choose_color = QComboBox()
        self.choose_color.addItems(options)
        self.choose_color.currentIndexChanged.connect(self.color_chosen)


        #Window Setup
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.welcome)
        self.vbox.addWidget(self.app_button)

        self.vbox.addWidget(self.color_message)
        self.vbox.addWidget(self.choose_color)
        self.vbox.addWidget(self.clear_button)
        self.vbox.addWidget(self.voice_button)
        self.vbox.addWidget(self.save_button1)
        self.vbox.addWidget(self.save_button2)

        self.setLayout(self.vbox)

    @pyqtSlot()
    def on_click(self):
        print("Clicked!!")
        self.our_window.clear_everything()
        self.our_window.paintWindow = np.zeros((471,636,3)) + 255
        self.our_window.camera = cv2.VideoCapture(0)
        self.our_window.draw()


    def save_image1(self):
        self.our_window.save1()


    def save_image2(self):
        self.our_window.save2()


    def voice_click(self):
        print("Voice Clicked!!")
        text = self.voiceObject.send_text();

        print(text)

        if text.lower() == "change color to blue":
            #self.our_window.colorIndex = 0;
            self.choose_color.setCurrentIndex(0);
            mixer.music.load('audio/blue.mp3')
            mixer.music.play()



        elif text.lower() == "change color to green":
            #self.our_window.colorIndex = 1;
            self.choose_color.setCurrentIndex(1);
            mixer.music.load('audio/green.mp3')
            mixer.music.play()


        elif text.lower() == "change color to red":
            #self.our_window.colorIndex = 2;
            self.choose_color.setCurrentIndex(2);
            mixer.music.load('audio/red.mp3')
            mixer.music.play()

        elif text.lower() == "change color to yellow":
            #self.our_window.colorIndex = 3;
            self.choose_color.setCurrentIndex(3);
            mixer.music.load('audio/yellow.mp3')
            mixer.music.play()

        elif text.lower() == "clear screen":
            self.our_window.clear_everything()
            mixer.music.load('audio/erase.mp3')
            mixer.music.play()

    def clean_screen(self):
        self.our_window.clear_everything()
        mixer.music.load('audio/erase.mp3')
        mixer.music.play()


    def color_chosen(self):
        new_color = self.choose_color.currentText()
        if(new_color == 'blue'):
            self.our_window.colorIndex = 0
        elif new_color == 'green':
            self.our_window.colorIndex = 1

        elif new_color == 'red':
            self.our_window.colorIndex = 2

        else:
            self.our_window.colorIndex = 3




app = QApplication(sys.argv)
main = Window()
main.show()
sys.exit(app.exec_())
