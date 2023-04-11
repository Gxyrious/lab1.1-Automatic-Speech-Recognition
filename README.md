# Human-Computer Interaction

## Lab1.1-Automatic Speech Recognition

### Introduction

- Dependencies Installation
  1. **PocketSphinx** is an embedded speech recognition engine with small computation and size.

     ```sh
     pip3 install pocketsphinx
     ```
  
  2. Install speech-to-text library dependency **SpeechRecognition**
  
     ```sh
     pip install SpeechRecognition
     ```
  
  3. Audio manipulation tool for **Python**
  
     ```sh
     brew install portaudio
     pip install pyaudio
     ```
  
  4. Qt visualization framework
  
     ```sh
     pip install pyqt5
     ```
  
- File directory
  
  ```shell
  .
  ├── README.md
  ├── asr.py
  ├── asrInterface.py
  ├── guessTheWord.py
  ├── icon
  │   ├── phone.png
  │   ├── play.gif
  │   └── voice.gif
  ├── resource
  │   ├── 1.png
  │   ├── 2.png
  │   └── 3.png
  ├── test.py
  └── wav
      ├── coding.wav
      ├── game.wav
      ├── index.wav
      ├── music.wav
      └── unknown.wav
  4 directories, 16 files
  ```
  
  test.py and guessTheWord.py are separate test files. 
  
  asr.py is the entry point program for the whole project.
  
- Runn the main program
  
  ```sh
  python asr.py
  ```
  
  <img src="./resource/1.png" style="zoom: 50%;" />
  
  Select the button **Test** at the bottom left and read the local directory `wav/index.wav` as user input, you can change the filename to try different inputs.
  
  <img src="./resource/2.png" style="zoom:50%;" />
  
  Or click the bottom right button **Start speaking**, and start speaking. The program automatically recognizes the end of voice input and converts the input into text to display to the user.
  
- Flow chart
  
  ![](./resource/3.png)

### The modifications to GUI and the codes

1. Add a button to the ui and bind it to the event in the main window. When the button is clicked, it will start recording (or read an audio file from a local file for testing).

   ```python
   # ui file
   self.speak_btn = QtWidgets.QPushButton(self.centralwidget)
   self.speak_btn.setGeometry(QtCore.QRect(150, 390, 100, 51))
   
   self.test_btn = QtWidgets.QPushButton(self.centralwidget)
   self.test_btn.setGeometry(QtCore.QRect(50, 390, 50, 50))
   
   self.speak_btn.setText(_translate("MainWindow", "Start speaking"))
   self.test_btn.setText(_translate("MainWindow", "Test"))
   ```

   ```python
   # Main window
   self.ui.speak_btn.clicked.connect(partial(self.getCommand))
   self.ui.test_btn.clicked.connect(partial(self.testCommand))
   ```

   *partial* is a **partial function** in *pyqt5*'s functools package, which can be used to create a callable object based on a function, fixing some parameters of the original function, and calling it with the unfixed parameters.

2. To get the user's audio (*getCommand* function), we call the `recognize_speech_from_mic` function and pass it to the recognizer and microphone. This part refers to the functions in the template to get the user's input from the microphone. And return it as text.

   ```python
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
     self.showCommand()
   ```

3. After that, it is displayed to the user to confirm whether the recognition is correct, and if the user chooses **Yes**, the command is executed.

   ```python
   def showCommand(self):
     showMessage = QtWidgets.QMessageBox()
     showMessage.setWindowTitle("Tips")
     showMessage.setText("You said: {}".format(self.myCommand))
     buttonY = QtWidgets.QPushButton('Yes')
     buttonN = QtWidgets.QPushButton('No')
     showMessage.addButton(buttonY, QtWidgets.QMessageBox.YesRole)
     showMessage.addButton(buttonN, QtWidgets.QMessageBox.NoRole)
     showMessage.exec_()
     if showMessage.clickedButton() == buttonY:
       self.execCommand()
   ```

4. Before executing an instruction, use the fuzzy matching function in `fuzzywuzzy` to select the most matching instruction from the `commands` library, and then determine whether the matching degree exceeds the preset threshold `score_threshold`. If it exceeds the threshold, it will be directly executed, otherwise it will prompt the user to not recognize it.

   ```python
   def execCommand(self):
     key, score, cmd = process.extractOne(self.myCommand, self.commands)
     if score > self.score_threshold:
       os.system(cmd)
     else:
       showMessage = QtWidgets.QMessageBox()
       showMessage.setWindowTitle("warn")
       showMessage.setText("Sorry, I can't recognize your command.")
       buttonY = QtWidgets.QPushButton('OK')
       showMessage.addButton(buttonY, QtWidgets.QMessageBox.YesRole)
       showMessage.exec_()
   ```

5. The preset variables are defined in *init* function.

   ```python
   self.score_threshold = 60
   self.commands = {
     "open /Applications/IntelliJ\ IDEA.app": "coding", 
     "open /Applications/NeteaseMusic.app": "play music",
     "open /Applications/Steam.app": "play game",
   }
   ```

6. For testing purposes, a test button was added to read audio as user input from the local file `./wav/index.wav`. There are three audio presets, one for each of the three commands, i.e

   | Speech Input | Instruction Execution                   |
   | :----------- | --------------------------------------- |
   | `coding`     | `open /Applications/IntelliJ\ IDEA.app` |
   | `play music` | `open /Applications/NeteaseMusic.app`   |
   | `play game`  | `open /Applications/Steam.app`          |


### The accuracy of speech recognition and how to improve it, if possible?

1. The pocketsphinx library used here has a low recognition accuracy due to its off-line lightweight version, and it is also difficult to recognize some consonants and words with curved tongue and flat tongue, such as *play*, *open*, etc. After dozens of attempts, it has not been able to identify the correct results. This may be due to the loud microphone noise (although the artificial sound is basically no noise), or the intonation is not accurate enough. The biggest reason I think is **the poor quality of the offline version of the model itself**, which cannot achieve high accuracy recognition.
2. If we want to improve the accuracy of recognition, we can start from the following aspects:

   1. **Adjusting pocketsphinx parameters**: pocketsphinx provides a number of parameters that you can try to adjust to improve the recognition accuracy. For example, a different language model (using paid apis such as Google, Bing, etc.), audio feature extractor, noise suppression, etc.

   2. **Another speech recognition library.** At present, the mainstream Python speech recognition libraries are:

      - CMU Sphinx (works offline)

      - Google Speech Recognition

      - Google Cloud Speech API

      - Wit.ai

      - Microsoft Azure Speech

      - Microsoft Bing Voice Recognition (Deprecated)

      - Houndify API

      - IBM Speech to Text

      - Snowboy Hotword Detection (works offline)

      These speech recognition libraries differ in their focus, with Google Cloud Voice focusing on speech-to-text conversion, and wit and apiai providing built-in functionality beyond basic speech recognition (natural language processing to identify the speaker's intent).

   3. **Train your own model.** In order to achieve higher accuracy and better match the application scenario. The training of the model needs to consider the following aspects:

      1. **Dataset:** Train the model on a large, high-quality dataset. Some publicly available speech datasets such as LibriSpeech, Mozilla Common Voice, etc., can be used.
      2. **Feature extraction:** The speech signal is a time domain signal, which needs to be converted into a frequency domain signal, that is, to extract features. Commonly used feature extraction methods include Mel-Frequency Cepstral Coefficients (MFCCs) and Linear Predictive Coding (LPC). When selecting a feature extraction method, the stability and representation ability of the features should be considered.
      3. **Model architecture:** The commonly used speech recognition models include Convolutional Neural Network (CNN), Recurrent Neural Network (RNN), Transformer, etc.
      4. **Data Augmentation:** The robustness and generalization ability of the model can be improved by augmenting the data with operations such as adding noise, variable speed, and pitch sandhe.

