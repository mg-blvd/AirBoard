

import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout,
                            QHBoxLayout, QPushButton, QComboBox, QLineEdit, QSlider)
from PyQt5.QtCore import pyqtSlot, Qt
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

        #Brush Size Slider
        self.slider_name = QLabel("Brush Size: 2")
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(50)
        self.slider.setFocusPolicy(Qt.StrongFocus)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.setTickInterval(10)
        self.slider.setSingleStep(1)
        self.slider.valueChanged.connect(self.on_slider_change)


        #Window Setup
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.welcome)
        self.vbox.addWidget(self.app_button)

        self.vbox.addWidget(self.color_message)
        self.vbox.addWidget(self.choose_color)
        self.vbox.addWidget(self.slider_name)
        self.vbox.addWidget(self.slider)
        self.vbox.addWidget(self.voice_button)
        self.vbox.addWidget(self.save_button1)
        self.vbox.addWidget(self.save_button2)

        self.setLayout(self.vbox)

    @pyqtSlot()
    def on_click(self):
        print("Clicked!!")
        self.our_window.paintWindow = np.zeros((471,636,3)) + 255
        self.our_window.camera = cv2.VideoCapture(0)
        self.our_window.draw()

    @pyqtSlot()
    def on_slider_change(self):
        slider_value = self.slider.value()
        self.slider_name.setText("Brush Size: " + str(slider_value))
        self.our_window.setBrush(slider_value)

    @pyqtSlot()
    def save_image1(self):
        self.our_window.save1()
    
    @pyqtSlot()
    def save_image2(self):
        self.our_window.save2()
    

    
    @pyqtSlot()
    def voice_click(self):
        print("Voice Clicked!!")
        mixer.music.load('audio/bell.wav')
        mixer.music.play()
        text = self.voiceObject.send_text();

        
        print(text)
        
        if "blue" in text.lower():
            #self.our_window.colorIndex = 0;
            self.choose_color.setCurrentIndex(0);
            mixer.music.load('audio/blue.mp3')
            mixer.music.play()


        
        elif "green" in text.lower():
            #self.our_window.colorIndex = 1;
            self.choose_color.setCurrentIndex(1);
            mixer.music.load('audio/green.mp3')
            mixer.music.play()

        
        elif "red" in text.lower():
            #self.our_window.colorIndex = 2;
            self.choose_color.setCurrentIndex(2);
            mixer.music.load('audio/red.mp3')
            mixer.music.play()

        elif "yellow" in text.lower():
            #self.our_window.colorIndex = 3;
            self.choose_color.setCurrentIndex(3);
            mixer.music.load('audio/yellow.mp3')
            mixer.music.play()
        elif "size" in text.lower():
            split_text = text.split(' ')
            for substr in split_text:
                if substr.isdigit():
                    new_size = int(substr)
                    self.slider.setValue(new_size)
                    self.slider_name.setText("Brush Size: " + str(new_size))
                    self.our_window.setBrush(new_size)


        elif "clear" in text.lower():
            #erase all
            self.our_window.bpoints = [deque(maxlen=512)]
            self.our_window.gpoints = [deque(maxlen=512)]
            self.our_windowrpoints = [deque(maxlen=512)]
            self.our_window.ypoints = [deque(maxlen=512)]
            
            self.our_window.bindex = 0
            self.our_window.gindex = 0
            self.our_window.rindex = 0
            self.our_window.yindex = 0
            
            self.our_window.paintWindow[67:,:,:] = 255
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









