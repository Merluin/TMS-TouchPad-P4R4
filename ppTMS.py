import sys
import serial
import threading
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QFont
import RPi.GPIO as GPIO
import time
from datetime import datetime
from PyQt5.QtCore import QMetaObject, Qt, Q_ARG

font = QFont()
font.setPointSize(18)
font.setBold(True)

# Relais Alim Arduino
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)

def relay_on():  # Function to turn the relay ON
    GPIO.output(17, GPIO.HIGH)

def relay_off():  # Function to turn the relay OFF
    GPIO.output(17, GPIO.LOW)

def cleanup_gpio():
    try:
        GPIO.cleanup()
    except RuntimeError as e:
        print(f"GPIO cleanup error: {e}")

# App
class SerialApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.isRunning = False
        self.thread = None

        # Initialize the serial connection
        self.arduinoSerial = serial.Serial()
        self.arduinoSerial.baudrate = 115200  # Need to match the Arduino code
        self.arduinoSerial.timeout = 1
        self.arduinoSerial.port = '/dev/ttyS0'  # Replace with the correct port

        # Attempt to open the serial port
        try:
            self.arduinoSerial.open()
        except serial.SerialException as e:
            print(f"Error opening serial port: {e}")

        # Create main widget and layout
        mainWidget = QtWidgets.QWidget()
        self.setCentralWidget(mainWidget)
        mainLayout = QtWidgets.QHBoxLayout(mainWidget)

        # Create splitter
        splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)

        # Left Panel for Sliders and Buttons
        leftPanel = QtWidgets.QWidget()
        leftLayout = QtWidgets.QVBoxLayout(leftPanel)

        # Add "Settings" label at the top of the left panel
        leftPanelLabel = QtWidgets.QLabel("Settings")
        leftPanelLabel.setFont(font)
        leftPanelLabel.setAlignment(QtCore.Qt.AlignCenter)
        leftLayout.addWidget(leftPanelLabel)

        self.createSpinBoxLayout(leftLayout, "IPI", 0, 200, 40)
        self.createSpinBoxLayout(leftLayout, "Nrep", 0, 150, 90)
        self.createSpinBoxLayout(leftLayout, "ITI", 0, 60, 10)

        # Add a label for "Trigger buttons:"
        triggerButtonsLabel = QtWidgets.QLabel("Test:")
        triggerButtonsLabel.setFont(font)
        leftLayout.addWidget(triggerButtonsLabel)

        # Create a horizontal layout for buttons
        buttonsLayout = QtWidgets.QHBoxLayout()

        # Create buttons and add them to the buttons layout
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

        # Add buttons layout to the left panel layout
        leftLayout.addLayout(buttonsLayout)

        # Create a label for displaying messages
        self.triggercatch = QtWidgets.QLabel()
        leftLayout.addWidget(self.triggercatch)

        # Add left panel to splitter
        splitter.addWidget(leftPanel)

        # Right Panel for future content
        rightPanel = QtWidgets.QWidget()
        rightLayout = QtWidgets.QVBoxLayout(rightPanel)

        # Add "ppTMS GUI" label at the top of the right panel
        rightPanelLabel = QtWidgets.QLabel("ppTMS")
        rightPanelLabel.setFont(font)
        rightPanelLabel.setAlignment(QtCore.Qt.AlignCenter)
        rightLayout.addWidget(rightPanelLabel)

        # Create Start and Stop buttons in the right panel
        self.startButton = QtWidgets.QPushButton('Start')
        self.startButton.setFont(font)
        self.startButton.setFixedHeight(80)
        self.startButton.clicked.connect(self.startButtonPushed)
        rightLayout.addWidget(self.startButton)

        self.stopButton = QtWidgets.QPushButton('Stop')
        self.stopButton.setFixedHeight(80)
        self.stopButton.setFont(font)
        self.stopButton.clicked.connect(self.stopButtonPushed)
        rightLayout.addWidget(self.stopButton)

        # Spacer at the bottom (expanding spacer)
        bottomSpacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        rightLayout.addItem(bottomSpacer)

        # Add right panel to splitter
        splitter.addWidget(rightPanel)

        # Add splitter to main layout
        mainLayout.addWidget(splitter)

        # Set the size of the window
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

    def TsButtonPushed(self):
        try:
            self.arduinoSerial.write(b'SET,test,1\n')
            self.triggercatch.setText('Ts pressed')
        except Exception as e:
            self.triggercatch.setText('!!! Serial is not connected !!!')

    def CsButtonPushed(self):
        try:
            self.arduinoSerial.write(b'SET,test,2\n')
            self.triggercatch.setText('Cs pressed')
        except Exception as e:
            self.triggercatch.setText('!!! Serial is not connected !!!')

    def TTLButtonPushed(self):
        try:
            self.arduinoSerial.write(b'SET,test,3\n')
            self.triggercatch.setText('Bio pressed')
        except Exception as e:
            self.triggercatch.setText('!!! Serial is not connected !!!')

    def startButtonPushed(self):
        ipi = self.ipiSpinBox.value()
        if not self.isRunning:
            self.isRunning = True
            self.thread = threading.Thread(target=self.runStimulationLoop, daemon=True)
            self.thread.start()

    def runStimulationLoop(self):
        numLoops = self.nrepSpinBox.value()
        iti = self.itiSpinBox.value()

        for i in range(numLoops):
            if not self.isRunning:
                return
            start_time = time.time()
            try:
                self.arduinoSerial.write(b'1\n')
            except serial.SerialException as e:
                print(f"Serial error: {e}")
                return
            QMetaObject.invokeMethod(self.startButton, "setText", Qt.QueuedConnection,
                                     Q_ARG(str, f"rep: {i+1}"))
            elapsed_time = time.time() - start_time
            remaining_time = max(0, iti - elapsed_time)
            time.sleep(remaining_time)

        self.isRunning = False
        QMetaObject.invokeMethod(self.startButton, "setText", Qt.QueuedConnection, Q_ARG(str, "Start"))

    def stopButtonPushed(self):
        self.isRunning = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=1)
            self.thread = None  # Clean up the thread reference

    def closeEvent(self, event):
        self.isRunning = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=1)
            self.thread = None  # Clean up the thread reference
        relay_off()  # Turn off the relay when the application is closed
        if self.arduinoSerial.is_open:
            self.arduinoSerial.close()  # Close the serial port if it's open
        cleanup_gpio()  # Clean up GPIO
        super().closeEvent(event)

if __name__ == '__main__':
    relay_on()  # Turn on the relay at the start of the application
    app = QtWidgets.QApplication(sys.argv)
    mainWin = SerialApp()
    mainWin.show()
    sys.exit(app.exec_())
