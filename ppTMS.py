import sys
import serial
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QThread, pyqtSignal
import RPi.GPIO as GPIO
import time
from datetime import datetime

# Font for UI
font = QFont()
font.setPointSize(18)
font.setBold(True)

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)

def relay_on():
    GPIO.output(17, GPIO.HIGH)

def relay_off():
    GPIO.output(17, GPIO.LOW)

# QThread for Stimulation Loop
class StimulationThread(QThread):
    progress_signal = pyqtSignal(int)
    message_signal = pyqtSignal(str)

    def __init__(self, nrep, iti, arduino_serial):
        super().__init__()
        self.nrep = nrep
        self.iti = iti
        self.arduino_serial = arduino_serial
        self.isRunning = True

    def run(self):
        for i in range(self.nrep):
            if not self.isRunning:
                break
            try:
                # Send trigger to Arduino
                self.arduino_serial.write(b'1\n')
                self.progress_signal.emit(int((i + 1) / self.nrep * 100))
                self.message_signal.emit(f"rep: {i + 1}")
                time.sleep(self.iti)
            except Exception as e:
                self.message_signal.emit(f"Error: {e}")
                break
        self.progress_signal.emit(100 if self.isRunning else 0)

    def stop(self):
        self.isRunning = False

# Main Application
class SerialApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.isRunning = False

        # Serial connection
        self.arduinoSerial = serial.Serial()
        self.arduinoSerial.baudrate = 115200
        self.arduinoSerial.timeout = 1
        self.arduinoSerial.port = '/dev/ttyS0'

        try:
            self.arduinoSerial.open()
        except serial.SerialException as e:
            print(f"Error opening serial port: {e}")

        # UI setup
        mainWidget = QtWidgets.QWidget()
        self.setCentralWidget(mainWidget)
        mainLayout = QtWidgets.QHBoxLayout(mainWidget)

        splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)

        # Left Panel
        leftPanel = QtWidgets.QWidget()
        leftLayout = QtWidgets.QVBoxLayout(leftPanel)

        leftPanelLabel = QtWidgets.QLabel("Settings")
        leftPanelLabel.setFont(font)
        leftPanelLabel.setAlignment(QtCore.Qt.AlignCenter)
        leftLayout.addWidget(leftPanelLabel)

        self.createSpinBoxLayout(leftLayout, "IPI", 0, 200, 40)
        self.createSpinBoxLayout(leftLayout, "Nrep", 0, 150, 90)
        self.createSpinBoxLayout(leftLayout, "ITI", 0, 60, 10)

        triggerButtonsLabel = QtWidgets.QLabel("Test:")
        triggerButtonsLabel.setFont(font)
        leftLayout.addWidget(triggerButtonsLabel)

        buttonsLayout = QtWidgets.QHBoxLayout()
        self.cs_button = QtWidgets.QPushButton('Cs')
        self.cs_button.setFixedHeight(80)
        self.cs_button.setFont(font)
        self.cs_button.clicked.connect(self.CsButtonPushed)
        buttonsLayout.addWidget(self.cs_button)

        self.ts_button = QtWidgets.QPushButton('Ts')
        self.ts_button.setFixedHeight(80)
        self.ts_button.setFont(font)
        self.ts_button.clicked.connect(self.TsButtonPushed)
        buttonsLayout.addWidget(self.ts_button)

        self.ttl_button = QtWidgets.QPushButton('Bio')
        self.ttl_button.setFixedHeight(80)
        self.ttl_button.setFont(font)
        self.ttl_button.clicked.connect(self.TTLButtonPushed)
        buttonsLayout.addWidget(self.ttl_button)

        leftLayout.addLayout(buttonsLayout)

        self.triggercatch = QtWidgets.QLabel()
        leftLayout.addWidget(self.triggercatch)

        splitter.addWidget(leftPanel)

        # Right Panel
        rightPanel = QtWidgets.QWidget()
        rightLayout = QtWidgets.QVBoxLayout(rightPanel)

        rightPanelLabel = QtWidgets.QLabel("ppTMS")
        rightPanelLabel.setFont(font)
        rightPanelLabel.setAlignment(QtCore.Qt.AlignCenter)
        rightLayout.addWidget(rightPanelLabel)

        self.progressBar = QtWidgets.QProgressBar()
        self.progressBar.setFixedHeight(50)
        self.progressBar.setFont(font)
        rightLayout.addWidget(self.progressBar)

        self.startButton = QtWidgets.QPushButton('Start')
        self.startButton.setFont(font)
        self.startButton.setFixedHeight(80)
        self.startButton.clicked.connect(self.startButtonPushed)
        rightLayout.addWidget(self.startButton)

        # self.pauseButton = QtWidgets.QPushButton('Pause')
        # self.pauseButton.setFixedHeight(80)
        # self.pauseButton.setFont(font)
        # self.pauseButton.clicked.connect(self.pauseButtonPushed)
        # rightLayout.addWidget(self.pauseButton)

        self.stopButton = QtWidgets.QPushButton('Stop')
        self.stopButton.setFixedHeight(80)
        self.stopButton.setFont(font)
        self.stopButton.clicked.connect(self.stopButtonPushed)
        rightLayout.addWidget(self.stopButton)

        splitter.addWidget(rightPanel)
        mainLayout.addWidget(splitter)

        self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle('GUI ppTMS Pi4R4')

    def createSpinBoxLayout(self, parentLayout, spinBoxName, minValue, maxValue, defaultValue):
        spinBoxLayout = QtWidgets.QHBoxLayout()
        spinBoxNameLabel = QtWidgets.QLabel(spinBoxName)
        spinBoxNameLabel.setFont(font)
        spinBoxLayout.addWidget(spinBoxNameLabel)

        spinBox = QtWidgets.QSpinBox()
        spinBox.setRange(minValue, maxValue)
        spinBox.setValue(defaultValue)
        spinBox.setFixedHeight(60)
        spinBox.setFont(font)
        spinBox.valueChanged.connect(lambda value, name=spinBoxName: self.spinBoxValueChanged(value, name))
        spinBoxLayout.addWidget(spinBox)

        valueLabel = QtWidgets.QLabel(str(defaultValue))
        valueLabel.setFont(font)
        spinBoxLayout.addWidget(valueLabel)

        parentLayout.addLayout(spinBoxLayout)
        setattr(self, f"{spinBoxName.lower()}SpinBox", spinBox)
        setattr(self, f"{spinBoxName.lower()}ValueLabel", valueLabel)

    def spinBoxValueChanged(self, value, name):
        label = getattr(self, f"{name.lower()}ValueLabel")
        label.setText(str(value))

    def writeToSerial(self, command):
        try:
            if self.arduinoSerial.is_open:
                self.arduinoSerial.write(command.encode())
            else:
                self.triggercatch.setText("Serial port not open!")
        except Exception as e:
            self.triggercatch.setText(f"Error: {e}")

    def CsButtonPushed(self):
        self.writeToSerial("SET,test,2\n")

    def TsButtonPushed(self):
        self.writeToSerial("SET,test,1\n")

    def TTLButtonPushed(self):
        self.writeToSerial("SET,test,3\n")

    def startButtonPushed(self):
        if not self.isRunning:
            self.isRunning = True
            self.stimulation_thread = StimulationThread(
                self.nrepSpinBox.value(),
                self.itiSpinBox.value(),
                self.arduinoSerial
            )
            self.stimulation_thread.progress_signal.connect(self.progressBar.setValue)
            self.stimulation_thread.message_signal.connect(self.startButton.setText)
            self.stimulation_thread.finished.connect(self.onStimulationFinished)
            self.stimulation_thread.start()

    def onStimulationFinished(self):
        self.isRunning = False
        self.startButton.setText("Start")

    def pauseButtonPushed(self):
        if self.isRunning:
            self.stimulation_thread.stop()
            self.startButton.setText("Paused")
        else:
            self.startButton.setText("Start")

    def stopButtonPushed(self):
        self.isRunning = False
        self.stimulation_thread.stop()
        self.progressBar.setValue(0)
        self.startButton.setText("Start")

    def closeEvent(self, event):
        relay_off()
        if self.arduinoSerial.is_open:
            self.arduinoSerial.close()
        GPIO.cleanup()
        super().closeEvent(event)


if __name__ == '__main__':
    relay_on()
    app = QtWidgets.QApplication(sys.argv)
    mainWin = SerialApp()
    mainWin.show()
    sys.exit(app.exec_())
