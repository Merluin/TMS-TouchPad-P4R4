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

        # Left Panel for QDial, Value Display, and Buttons
        leftPanel = QtWidgets.QWidget()
        leftLayout = QtWidgets.QVBoxLayout(leftPanel)

        # Create a horizontal layout for the dial and its value label
        dialLayout = QtWidgets.QHBoxLayout()

        # Create QDial
        self.dial = QtWidgets.QDial()
        self.dial.setRange(0, 200)
        self.dial.valueChanged.connect(self.dialValueChanged)

        # Create Label for QDial Name
        dialNameLabel = QtWidgets.QLabel("IPI")
        dialLayout.addWidget(dialNameLabel)

        # Add QDial to the layout
        dialLayout.addWidget(self.dial)

        # Create Value Display Label
        self.dialValueLabel = QtWidgets.QLabel("0")
        dialLayout.addWidget(self.dialValueLabel)

        # Add the dial layout to the left panel layout
        leftLayout.addLayout(dialLayout)

        # Create buttons and add them to the left panel
        self.ts_button = QtWidgets.QPushButton('TsButton')
        self.ts_button.clicked.connect(self.TsButtonPushed)
        leftLayout.addWidget(self.ts_button)

        self.cs_button = QtWidgets.QPushButton('CsButton')
        self.cs_button.clicked.connect(self.CsButtonPushed)
        leftLayout.addWidget(self.cs_button)

        self.ttl_button = QtWidgets.QPushButton('TTLButton')
        self.ttl_button.clicked.connect(self.TTLButtonPushed)
        leftLayout.addWidget(self.ttl_button)

        # Create a label for displaying messages
        self.triggercatch = QtWidgets.QLabel()
        leftLayout.addWidget(self.triggercatch)

        # Add left panel to splitter
        splitter.addWidget(leftPanel)

        # Right Panel for future content
        rightPanel = QtWidgets.QWidget()
        splitter.addWidget(rightPanel)

        # Add splitter to main layout
        mainLayout.addWidget(splitter)

        # Set the size of the window
        self.setGeometry(100, 100, 800, 400)
        self.setWindowTitle('Serial Communication App')

    def dialValueChanged(self, value):
        self.dialValueLabel.setText(str(value))

    # ... [rest of your class methods] ...

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWin = SerialApp()
    mainWin.show()
    sys.exit(app.exec_())
