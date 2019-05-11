import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout,
                            QHBoxLayout, QPushButton, QComboBox, QLineEdit, QSlider)
from PyQt5.QtCore import pyqtSlot, Qt
from paint import DrawingWindow
import numpy as np
import cv2
import threading
import speech as VoiceRecord
from collections import deque
from pygame import mixer





class Window(QWidget):
    def __init__(self):
        super().__init__()
        mixer.init()

        self.our_window = DrawingWindow()
        self.voiceObject = VoiceRecord.VoiceRecord();

        # Window Title
        self.setWindowTitle("Home Page")

        #Thread for voice commands
        self.voice_thread = threading.Thread(target=self.voice_control)

        # Welcome Message
        self.welcome = QLabel("Welcome!!\nClick on the button below to access the app.")
        self.color_message = QLabel("Change the color of the line.")


        # Button that takes you to the app.
        self.app_button = QPushButton("Start Drawing!!")
        self.app_button.clicked.connect(self.on_click)

        # Button that deleates clear_everything
        self.clear_button = QPushButton("Clear the Screen")
        self.clear_button.clicked.connect(self.clean_screen)


        # Button to listen for voice commands
        self.voice_button = QPushButton("Voice Command")
        self.voice_button.clicked.connect(self.voice_click)

        # Button to listen for save
        self.save_button1 = QPushButton("Save drawing")
        self.save_button1.clicked.connect(self.save_image1)
        self.save_button2 = QPushButton("Save drawing with background")
        self.save_button2.clicked.connect(self.save_image2)


        # Colors Combobox
        options = ["blue", "green", "red", "yellow"]
        self.choose_color = QComboBox()
        self.choose_color.addItems(options)
        self.choose_color.currentIndexChanged.connect(self.color_chosen)

        # Slider for Brush Size
        self.slider_name = QLabel("Brush Size: 2")
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(50)
        self.slider.setValue(2)
        self.slider.setFocusPolicy(Qt.StrongFocus)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.setTickInterval(10)
        self.slider.setSingleStep(1)
        self.slider.valueChanged.connect(self.on_slider_change)

        #Close windows Button
        self.close_button = QPushButton("Close the Windows")
        self.close_button.clicked.connect(self.close_the_wins)



        # Window Setup
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.welcome)
        self.vbox.addWidget(self.app_button)
        self.vbox.addWidget(self.color_message)
        self.vbox.addWidget(self.choose_color)
        self.vbox.addWidget(self.slider_name)
        self.vbox.addWidget(self.slider)
        self.vbox.addWidget(self.clear_button)
        self.vbox.addWidget(self.voice_button)
        self.vbox.addWidget(self.save_button1)
        self.vbox.addWidget(self.save_button2)
        self.vbox.addWidget(self.close_button)

        self.setLayout(self.vbox)

    @pyqtSlot()
    def on_click(self):
        self.our_window.close_wins = False
        self.our_window.camera = cv2.VideoCapture(0)
        self.our_window.draw()

    @pyqtSlot()
    def on_slider_change(self):
        slider_value = self.slider.value()
        self.slider_name.setText(f"Brush Size: {slider_value}")
        self.our_window.setBrush(slider_value)

    @pyqtSlot()
    def save_image1(self):
        self.our_window.save1()
        mixer.music.load('audio/save.mp3')
        mixer.music.play()
    @pyqtSlot()
    def save_image2(self):
        self.our_window.save2()
        mixer.music.load('audio/save.mp3')
        mixer.music.play()
    @pyqtSlot()
    def voice_click(self):
        self.voice_thread.start()
        self.voice_thread = threading.Thread(target=self.voice_control)

    @pyqtSlot()
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

    def close_the_wins(self):
        self.our_window.close_wins = True
        self.our_window.clear_everything()

    def voice_control(self):
        print("Voice Button Clicked!!")
        mixer.music.load('audio/bell.wav')
        mixer.music.play()
        text = self.voiceObject.send_text();
        print(text)

        text = text.lower()

        if "blue" in text:
            #self.our_window.colorIndex = 0;
            self.choose_color.setCurrentIndex(0);
            mixer.music.load('audio/blue.mp3')
            mixer.music.play()

        elif "green" in text:
            #self.our_window.colorIndex = 1;
            self.choose_color.setCurrentIndex(1);
            mixer.music.load('audio/green.mp3')
            mixer.music.play()

        elif "red" in text:
            #self.our_window.colorIndex = 2;
            self.choose_color.setCurrentIndex(2);
            mixer.music.load('audio/red.mp3')
            mixer.music.play()

        elif "yellow" in text:
            #self.our_window.colorIndex = 3;
            self.choose_color.setCurrentIndex(3);
            mixer.music.load('audio/yellow.mp3')
            mixer.music.play()

        # Changing Brush Size: Say size and a number between 1 and 50 in the same sentence
        elif "size" in text:
            for substr in text.split(' '):
                if substr.isdigit():
                    new_size = int(substr)
                    if new_size <= 50 and new_size > 0:
                        self.slider.setValue(new_size)
                        self.slider_name.setText("Brush Size: " + str(new_size))
                        self.our_window.setBrush(new_size)
                        mixer.music.load('audio/{}.mp3'.format(substr))
                        mixer.music.play()
                    else:
                        print(substr + " is an invalid size")
        # Clears all drawings
        elif "clear" in text or "clean" in text:
            self.our_window.clear_everything()
            mixer.music.load('audio/erase.mp3')
            mixer.music.play()

        elif "close" in text:
            self.close_the_wins()

        elif "open" in text:
            self.on_click()

    @pyqtSlot()
    def clean_screen(self):
        self.our_window.clear_everything()
        mixer.music.load('audio/erase.mp3')
        mixer.music.play()




app = QApplication(sys.argv)
main = Window()
p =  main.palette()
p.setColor(main.backgroundRole(), Qt.white)
main.setPalette(p)
main.show()
sys.exit(app.exec_())
