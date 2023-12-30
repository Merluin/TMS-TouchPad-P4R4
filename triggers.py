import sys
import serial
from PyQt5 import QtWidgets, QtCore

class SerialApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize the serial connection
        self.arduinoSerial = serial.Serial()
        self.arduinoSerial.baudrate = 9600
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
        self.createDialLayout(leftLayout, "IPI", 0, 200, 4)

        # Create layout and widgets for Nrep Dial (default value 90)
        self.createDialLayout(leftLayout, "Nrep", 0, 100, 90)

        # Create layout and widgets for ITI Dial (default value 10)
        self.createDialLayout(leftLayout, "ITI", 0, 300, 10)

        # Create a horizontal layout for buttons
        buttonsLayout = QtWidgets.QHBoxLayout()

        # Create buttons and add them to the buttons layout
        self.ts_button = QtWidgets.QPushButton('TsButton')
        self.ts_button.clicked.connect(self.TsButtonPushed)
        buttonsLayout.addWidget(self.ts_button)

        self.cs_button = QtWidgets.QPushButton('CsButton')
        self.cs_button.clicked.connect(self.CsButtonPushed)
        buttonsLayout.addWidget(self.cs_button)

        self.ttl_button = QtWidgets.QPushButton('TTLButton')
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

        # Add right panel to splitter
        splitter.addWidget(rightPanel)

        # Add splitter to main layout
        mainLayout.addWidget(splitter)

        # Set the size of the window
        self.setGeometry(100, 100, 800, 400)
        self.setWindowTitle('Serial Communication App')

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
            self.arduinoSerial.write(b'SET,test,1\n')
            self.triggercatch.setText('TsButton pressed')
        except Exception as e:
            self.triggercatch.setText('!!! Serial is not connected !!!')

    def CsButtonPushed(self):
        try:
            self.arduinoSerial.write(b'SET,test,2\n')
            self.triggercatch.setText('CsButton pressed')
        except Exception as e:
            self.triggercatch.setText('!!! Serial is not connected !!!')

    def TTLButtonPushed(self):
        try:
            self.arduinoSerial.write(b'SET,test,3\n')
            self.triggercatch.setText('TTLButton pressed')
        except Exception as e:
            self.triggercatch.setText('!!! Serial is not connected !!!')

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWin = SerialApp()
    mainWin.show()
    sys.exit(app.exec_())
