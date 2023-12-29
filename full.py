import sys
import serial.tools.list_ports
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QSpinBox,
    QSplitter,
)

class ppTMSApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.arduinoSerial = None

        self.initUI()

    def initUI(self):
        self.setWindowTitle("ppTMS App")
        self.setGeometry(100, 100, 800, 400)

        # Create central widget and layouts
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)

        splitter = QSplitter()
        left_panel = QWidget()

        splitter.addWidget(left_panel)

        layout.addWidget(splitter)

        left_layout = QVBoxLayout(left_panel)

        # Left Panel
        self.serial_button = QPushButton("Serial")
        self.connect_button = QPushButton("Connect")
        self.serialcatch = QLabel()

        parameters_label = QLabel("Parameters")
        iti_label = QLabel("ITI")
        self.iti_spinner = QSpinBox()
        nrep_label = QLabel("Nrep")
        self.nrep_spinner = QSpinBox()
        ipi_label = QLabel("IPI")
        self.ipi_spinner = QSpinBox()

        left_layout.addWidget(self.serial_button)
        left_layout.addWidget(self.connect_button)
        left_layout.addWidget(self.serialcatch)

        left_layout.addWidget(parameters_label)
        left_layout.addWidget(iti_label)
        left_layout.addWidget(self.iti_spinner)
        left_layout.addWidget(nrep_label)
        left_layout.addWidget(self.nrep_spinner)
        left_layout.addWidget(ipi_label)
        left_layout.addWidget(self.ipi_spinner)

        self.connect_button.clicked.connect(self.ConnectButtonPushed)
        self.serial_button.clicked.connect(self.SerialButtonPushed)

    def ConnectButtonPushed(self):
        # Automatically detect the Arduino serial port
        arduino_ports = [
            p.device
            for p in serial.tools.list_ports.comports()
            if "Arduino" in p.description
        ]
        if arduino_ports:
            self.serialcatch.setText(f"Serial connected to {arduino_ports[0]}")
            try:
                # Initialize the Arduino serial port using the detected port
                self.arduinoSerial = serial.Serial(arduino_ports[0], 115200)

                # Open the serial connection
                self.arduinoSerial.open()
            except Exception as e:
                # If there's an error while opening the serial connection, handle it here
                # For example, you can display an error message.
                self.serialcatch.setText("!!! Error opening serial connection !!!")
        else:
            self.serialcatch.setText("!!! No Arduino found !!!")

    def SerialButtonPushed(self):
        # Manually set the Arduino serial port
        self.arduinoSerial = serial.Serial(self.serial_edit.text(), 115200)
        self.arduinoSerial.open()
        self.serialcatch.setText(f"Serial connected to {self.serial_edit.text()}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ppTMSApp()
    window.show()
    sys.exit(app.exec_())
