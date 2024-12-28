import sys
import serial
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QPushButton, QProgressBar, QSplitter
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QThread, pyqtSignal, Qt
import RPi.GPIO as GPIO
import time

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

    def __init__(self, nrep_spinbox, iti_spinbox, arduino_serial, ipi_spinbox):
        super().__init__()

        self.arduino_serial = arduino_serial
        self.isRunning = True

    def run(self):
        nrep = self.nrep_spinbox.value()  # Initial number of repetitions
        for i in range(nrep):
            if not self.isRunning:
                break
            try:
                # Fetch the latest values dynamically
                iti = self.iti_spinbox.value()
                ipi = self.ipi_spinbox.value()

                # Debug: Log the values to ensure they are updated
                print(f"Iteration {i + 1}: ITI={iti}, IPI={ipi}")

                # Send trigger to Arduino
                self.arduino_serial.write(b'1\n')
                time.sleep(ipi)  # Inter-Pulse Interval

                # Emit progress and message
                self.progress_signal.emit(int((i + 1) / nrep * 100))
                self.message_signal.emit(f"rep: {i + 1}")

                # Wait for remaining ITI time
                remaining_iti = max(0, iti - ipi)
                time.sleep(remaining_iti)
            except Exception as e:
                self.message_signal.emit(f"Error: {e}")
                break

        # Emit final progress status
        self.progress_signal.emit(100 if self.isRunning else 0)

    def stop(self):
        self.isRunning = False


# Main Application
class SerialApp(QMainWindow):
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
        mainWidget = QWidget()
        self.setCentralWidget(mainWidget)
        mainLayout = QHBoxLayout(mainWidget)

        splitter = QSplitter(Qt.Horizontal)

        # Left Panel
        leftPanel = QWidget()
        leftLayout = QVBoxLayout(leftPanel)

        leftPanelLabel = QLabel("Settings")
        leftPanelLabel.setFont(font)
        leftPanelLabel.setAlignment(Qt.AlignCenter)
        leftLayout.addWidget(leftPanelLabel)

        self.createSpinBoxLayout(leftLayout, "IPI", 0, 200, 40)
        self.createSpinBoxLayout(leftLayout, "Nrep", 0, 150, 90)
        self.createSpinBoxLayout(leftLayout, "ITI", 0, 60, 10)

        triggerButtonsLabel = QLabel("Test:")
        triggerButtonsLabel.setFont(font)
        leftLayout.addWidget(triggerButtonsLabel)

        buttonsLayout = QHBoxLayout()
        self.cs_button = QPushButton('Cs')
        self.cs_button.setFixedHeight(80)
        self.cs_button.setFont(font)
        self.cs_button.clicked.connect(self.CsButtonPushed)
        buttonsLayout.addWidget(self.cs_button)

        self.ts_button = QPushButton('Ts')
        self.ts_button.setFixedHeight(80)
        self.ts_button.setFont(font)
        self.ts_button.clicked.connect(self.TsButtonPushed)
        buttonsLayout.addWidget(self.ts_button)

        self.ttl_button = QPushButton('Bio')
        self.ttl_button.setFixedHeight(80)
        self.ttl_button.setFont(font)
        self.ttl_button.clicked.connect(self.TTLButtonPushed)
        buttonsLayout.addWidget(self.ttl_button)

        leftLayout.addLayout(buttonsLayout)

        self.triggercatch = QLabel()
        leftLayout.addWidget(self.triggercatch)

        splitter.addWidget(leftPanel)

        # Right Panel
        rightPanel = QWidget()
        rightLayout = QVBoxLayout(rightPanel)

        rightPanelLabel = QLabel("ppTMS")
        rightPanelLabel.setFont(font)
        rightPanelLabel.setAlignment(Qt.AlignCenter)
        rightLayout.addWidget(rightPanelLabel)

        self.progressBar = QProgressBar()
        self.progressBar.setFixedHeight(50)
        self.progressBar.setFont(font)
        rightLayout.addWidget(self.progressBar)

        self.startButton = QPushButton('Start')
        self.startButton.setFont(font)
        self.startButton.setFixedHeight(80)
        self.startButton.clicked.connect(self.startButtonPushed)
        rightLayout.addWidget(self.startButton)

        self.stopButton = QPushButton('Stop')
        self.stopButton.setFixedHeight(80)
        self.stopButton.setFont(font)
        self.stopButton.clicked.connect(self.stopButtonPushed)
        rightLayout.addWidget(self.stopButton)

        splitter.addWidget(rightPanel)
        mainLayout.addWidget(splitter)

        self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle('GUI ppTMS Pi4R4')

    def createSpinBoxLayout(self, parentLayout, spinBoxName, minValue, maxValue, defaultValue):
        spinBoxLayout = QHBoxLayout()
        spinBoxNameLabel = QLabel(spinBoxName)
        spinBoxNameLabel.setFont(font)
        spinBoxLayout.addWidget(spinBoxNameLabel)

        spinBox = QSpinBox()
        spinBox.setRange(minValue, maxValue)
        spinBox.setValue(defaultValue)
        spinBox.setFixedHeight(60)
        spinBox.setFont(font)
        spinBox.valueChanged.connect(lambda value, name=spinBoxName: self.spinBoxValueChanged(value, name))
        spinBoxLayout.addWidget(spinBox)

        valueLabel = QLabel(str(defaultValue))
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
        # Fetch current values from spin boxes
        nrep_value = self.nrepSpinBox.value()
        iti_value = self.itiSpinBox.value()
        ipi_value = self.ipiSpinBox.value()

        # Debug: Log the values to verify they are updated
        print(f"Start pressed with values - Nrep: {nrep_value}, ITI: {iti_value}, IPI: {ipi_value}")

        # Start the stimulation thread with updated values
        self.isRunning = True
        self.stimulation_thread = StimulationThread(
            nrep_value,    # Updated number of repetitions
            iti_value,     # Updated inter-trial interval
            self.arduinoSerial,  # Arduino serial connection
            ipi_value      # Updated inter-pulse interval
        )
        self.stimulation_thread.progress_signal.connect(self.progressBar.setValue)
        self.stimulation_thread.message_signal.connect(self.startButton.setText)
        self.stimulation_thread.finished.connect(self.onStimulationFinished)
        self.stimulation_thread.start()


    def onStimulationFinished(self):
        self.isRunning = False
        self.startButton.setText("Start")

    def stopButtonPushed(self):
        if self.isRunning:
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

# Main program execution
if __name__ == '__main__':
    relay_on()
    app = QApplication(sys.argv)
    mainWin = SerialApp()
    mainWin.show()
    sys.exit(app.exec_())
