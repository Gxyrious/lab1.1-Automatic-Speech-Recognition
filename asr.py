from PyQt5 import QtWidgets, QtGui, QtCore, uic
from functools import partial

from asrInterface import Ui_MainWindow
import sys, os

import speech_recognition as sr

from fuzzywuzzy import process

class myWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(myWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.speak_btn.clicked.connect(partial(self.getCommand))
        self.ui.test_btn.clicked.connect(partial(self.testCommand))
        self.score_threshold = 60
        self.commands = {
            "open /Applications/IntelliJ\ IDEA.app": "coding", 
            "open /Applications/NeteaseMusic.app": "play music",
            "open /Applications/Steam.app": "play game",
        }
        
    def recognize_speech_from_mic(self, recognizer, microphone):
        if not isinstance(recognizer, sr.Recognizer):
            raise TypeError("`recognizer` must be `Recognizer` instance")

        if not isinstance(microphone, sr.Microphone):
            raise TypeError("`microphone` must be `Microphone` instance")

        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        response = {
            "success": True,
            "error": None,
            "transcription": None
        }

        try:
            response["transcription"] = recognizer.recognize_sphinx(audio)
        except sr.RequestError:
            # API was unreachable or unresponsive
            response["success"] = False
            response["error"] = "API unavailable"
        except sr.UnknownValueError:
            # speech was unintelligible
            response["error"] = "Unable to recognize speech"

        return response
    
    def recognize_speech_from_audio(self, recognizer, path):
        if not isinstance(recognizer, sr.Recognizer):
            raise TypeError("`recognizer` must be `Recognizer` instance")

        speech = sr.AudioFile(path)
        with speech as source:
            audio = recognizer.record(source)

        response = {
            "success": True,
            "error": None,
            "transcription": None
        }

        try:
            response["transcription"] = recognizer.recognize_sphinx(audio)
        except sr.RequestError:
            # API was unreachable or unresponsive
            response["success"] = False
            response["error"] = "API unavailable"
        except sr.UnknownValueError:
            # speech was unintelligible
            response["error"] = "Unable to recognize speech"

        return response
    
    def getCommand(self):
        microphone = sr.Microphone()
        recognizer = sr.Recognizer()
        for _ in range(5):
            order = self.recognize_speech_from_mic(recognizer, microphone)
            if order["transcription"]:
                break
            if not order["success"]:
                break
            print("I didn't catch that. What did you say?\n")
        if order["error"]:
            print("ERROR: {}".format(order["error"]))
            
        print("You said: {}".format(order["transcription"]))
        self.myCommand = order["transcription"]
        key, score, cmd = process.extractOne(self.myCommand, self.commands)
        print(key, score, cmd)
        self.showCommand()

    def testCommand(self):
        recognizer = sr.Recognizer()
        for i in range(5):
            order = self.recognize_speech_from_audio(recognizer, "wav/index.wav")
            if order["transcription"]:
                break
            if not order["success"]:
                break
            print("I didn't catch that. What did you say?\n")
        if order["error"]:
            print("ERROR: {}".format(order["error"]))
            
        print("You said: {}".format(order["transcription"]))
        self.myCommand = order["transcription"]
        self.showCommand()
    
    def showCommand(self):
        showMessage = QtWidgets.QMessageBox()
        showMessage.setWindowTitle("提示")
        showMessage.setText("You said: {}".format(self.myCommand))
        buttonY = QtWidgets.QPushButton('Yes')
        buttonN = QtWidgets.QPushButton('No')
        showMessage.addButton(buttonY, QtWidgets.QMessageBox.YesRole)
        showMessage.addButton(buttonN, QtWidgets.QMessageBox.NoRole)
        showMessage.exec_()
        if showMessage.clickedButton() == buttonY:
            self.execCommand()
    
    def execCommand(self):
        key, score, cmd = process.extractOne(self.myCommand, self.commands)
        if score > self.score_threshold:
            os.system(cmd)
        else:
            # 提示无法识别
            showMessage = QtWidgets.QMessageBox()
            showMessage.setWindowTitle("警告")
            showMessage.setText("Sorry, I can't recognize your command.")
            buttonY = QtWidgets.QPushButton('OK')
            showMessage.addButton(buttonY, QtWidgets.QMessageBox.YesRole)
            showMessage.exec_()
            

app = QtWidgets.QApplication([])
application = myWindow()
application.show()
sys.exit(app.exec())

