import sys
import serial
from PyQt5 import QtWidgets, QtCore
import RPi.GPIO as GPIO
import time
import threading

# Set up GPIO using BCM numbering
GPIO.setmode(GPIO.BCM)

# Set up pin 17 as an output
GPIO.setup(17, GPIO.OUT)

# Function to turn the relay ON
def relay_on():
    GPIO.output(17, GPIO.HIGH)  # Set GPIO 17 to HIGH

# Function to turn the relay OFF
def relay_off():
    GPIO.output(17, GPIO.LOW)   # Set GPIO 17 to LOW

class SerialApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.isRunning = False

        # Initialize the serial connection
        self.arduinoSerial = serial.Serial()
        self.arduinoSerial.baudrate = 115200
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

        # Left Panel for Dials and Buttons
        leftPanel = QtWidgets.QWidget()
        leftLayout = QtWidgets.QVBoxLayout(leftPanel)

        # Add "Settings" label at the top of the left panel
        leftPanelLabel = QtWidgets.QLabel("Settings")
        leftPanelLabel.setAlignment(QtCore.Qt.AlignCenter)
        leftLayout.addWidget(leftPanelLabel)

        # Create layout and widgets for IPI Dial (default value 4)
        self.createDialLayout(leftLayout, "IPI", 0, 1000, 300)

        # Create layout and widgets for Nrep Dial (default value 90)
        self.createDialLayout(leftLayout, "Nrep", 0, 200, 10)

        # Create layout and widgets for ITI Dial (default value 10)
        self.createDialLayout(leftLayout, "ITI", 0, 120, 5)

        # Add a label for "Trigger buttons:"
        triggerButtonsLabel = QtWidgets.QLabel("Trigger buttons:")
        leftLayout.addWidget(triggerButtonsLabel)

        # Create a horizontal layout for buttons
        buttonsLayout = QtWidgets.QHBoxLayout()

        # Create buttons and add them to the buttons layout
        self.cs_button = QtWidgets.QPushButton('Cs')
        self.cs_button.clicked.connect(self.CsButtonPushed)
        buttonsLayout.addWidget(self.cs_button)
        
        self.ts_button = QtWidgets.QPushButton('Ts')
        self.ts_button.clicked.connect(self.TsButtonPushed)
        buttonsLayout.addWidget(self.ts_button)

        self.ttl_button = QtWidgets.QPushButton('Bio')
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
        rightPanelLabel = QtWidgets.QLabel("ppTMS GUI")
        rightPanelLabel.setAlignment(QtCore.Qt.AlignCenter)
        rightLayout.addWidget(rightPanelLabel)

        # Create Start, Pause, Stop buttons in the right panel
        self.startButton = QtWidgets.QPushButton('Start')
        self.startButton.clicked.connect(self.startButtonPushed)
        rightLayout.addWidget(self.startButton)

        # Create a progress bar under the Start button
        self.progressBar = QtWidgets.QProgressBar()
        rightLayout.addWidget(self.progressBar)

        self.pauseButton = QtWidgets.QPushButton('Pause')
        rightLayout.addWidget(self.pauseButton)

        self.stopButton = QtWidgets.QPushButton('Stop')
        self.stopButton.clicked.connect(self.stopButtonPushed)
        rightLayout.addWidget(self.stopButton)

        # Add right panel to splitter
        splitter.addWidget(rightPanel)

        # Add splitter to main layout
        mainLayout.addWidget(splitter)

        # Set the size of the window
        self.setGeometry(100, 100, 800, 400)
        self.setWindowTitle('Serial Communication App')
        
        self.loopPaused = threading.Event()
        self.loopPaused.set()  # Initially set to True to allow loop execution
        self.loopCondition = threading.Condition()
        self.pauseButton.clicked.connect(self.pauseButtonPushed)

        
    def adjustSplitter(self):
      window_width = self.width()
      self.splitter.setSizes([window_width // 2, window_width // 2])

    def createDialLayout(self, parentLayout, dialName, minValue, maxValue, defaultValue):
        # Create a horizontal layout for the dial and its value label
        dialLayout = QtWidgets.QHBoxLayout()

        # Create Label for QDial Name
        dialNameLabel = QtWidgets.QLabel(dialName)
        dialLayout.addWidget(dialNameLabel)

        # Create QDial
        dial = QtWidgets.QDial()
        dial.setRange(minValue, maxValue)
        dial.setValue(defaultValue)  # Set default value
        dial.valueChanged.connect(lambda value, name=dialName: self.dialValueChanged(value, name))
        dialLayout.addWidget(dial)

        # Create Value Display Label with default value
        valueLabel = QtWidgets.QLabel(str(defaultValue))
        dialLayout.addWidget(valueLabel)

        # Add the dial layout to the parent layout
        parentLayout.addLayout(dialLayout)

        # Store dial and label in a dictionary for later reference
        setattr(self, f"{dialName.lower()}Dial", dial)
        setattr(self, f"{dialName.lower()}ValueLabel", valueLabel)

    def dialValueChanged(self, value, name):
        label = getattr(self, f"{name.lower()}ValueLabel")
        label.setText(str(value))

    def TsButtonPushed(self):
        try:
            self.arduinoSerial.write(b'SET,test,1')
            self.triggercatch.setText('Ts pressed')
        except Exception as e:
            self.triggercatch.setText('!!! Serial is not connected !!!')

    def CsButtonPushed(self):
        try:
            self.arduinoSerial.write(b'SET,test,2')
            self.triggercatch.setText('Cs pressed')
        except Exception as e:
            self.triggercatch.setText('!!! Serial is not connected !!!')

    def TTLButtonPushed(self):
        try:
            self.arduinoSerial.write(b'SET,test,3')
            self.triggercatch.setText('Bio pressed')
        except Exception as e:
            self.triggercatch.setText('!!! Serial is not connected !!!')
            
    def startButtonPushed(self):
        if not self.isRunning:
            self.isRunning = True
            self.startButton.setStyleSheet("background-color:#ff0000;")
            ipi = self.ipiDial.value()
            
            # Send the IPI command
            self.arduinoSerial.write(f'SET,IPI1,{ipi}'.encode())
            # Start the stimulation loop in a separate thread
            self.thread = threading.Thread(target=self.runStimulationLoop)
            self.thread.start()

    def runStimulationLoop(self):
        numLoops = self.nrepDial.value()
        iti = self.itiDial.value()
    
        for i in range(numLoops):
            with self.loopCondition:
                while not self.loopPaused.is_set():
                    self.loopCondition.wait()  # Wait if paused
    
            if not self.isRunning:
                break
    
            self.arduinoSerial.write(b'START1')
            time.sleep(iti)
            progress = int((i / numLoops) * 100)
            self.progressBar.setValue(progress)
            QtWidgets.QApplication.processEvents()
    
        self.progressBar.setValue(100) if self.isRunning else self.progressBar.setValue(0)
        self.isRunning = False
        self.startButton.setStyleSheet("background-color: gray")
        
    def pauseLoop(self):
        self.loopPaused.clear()  # Clear the event to pause the loop

    def resumeLoop(self):
        with self.loopCondition:
            self.loopPaused.set()  # Set the event to resume the loop
            self.loopCondition.notify()  # Notify the loop to continue

    def pauseButtonPushed(self):
        if self.isRunning and self.loopPaused.is_set():
            self.pauseLoop()
            self.pauseButton.setText("Resume")
        else:
            self.resumeLoop()
            self.pauseButton.setText("Pause")

    def stopButtonPushed(self):
        self.isRunning = False
        self.stopButton.setStyleSheet("background-color: red")


    def closeEvent(self, event):
        relay_off()  # Turn off the relay when the application is closed
        if self.arduinoSerial.is_open:
            self.arduinoSerial.close()  # Close the serial port if it's open
        GPIO.cleanup()  # Clean up GPIO
        super().closeEvent(event)

if __name__ == '__main__':
    relay_on()  # Turn on the relay at the start of the application
    app = QtWidgets.QApplication(sys.argv)
    mainWin = SerialApp()
    mainWin.show()
    sys.exit(app.exec_())

