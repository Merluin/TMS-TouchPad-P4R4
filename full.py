import sys
import serial
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
from PyQt5.QtCore import QTimer

class ppTMSApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.arduinoSerial = None
        self.isRunning = False
        self.isbreak = False
        self.pausa = False

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
        right_panel = QWidget()

        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)

        layout.addWidget(splitter)

        left_layout = QVBoxLayout(left_panel)
        right_layout = QVBoxLayout(right_panel)

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

        self.triggercatch = QLabel()
        self.ts_button = QPushButton("Ts")
        self.cs_button = QPushButton("Cs")
        self.ttl_button = QPushButton("TTL")

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

        left_layout.addWidget(self.triggercatch)
        left_layout.addWidget(self.ts_button)
        left_layout.addWidget(self.cs_button)
        left_layout.addWidget(self.ttl_button)

        # Right Panel
        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")
        self.pause_button = QPushButton("Pause")
        self.labelrep = QLabel("0")
        self.label = QLabel()
        self.progress_label = QLabel("Progress:")

        right_layout.addWidget(self.start_button)
        right_layout.addWidget(self.stop_button)
        right_layout.addWidget(self.pause_button)
        right_layout.addWidget(self.labelrep)
        right_layout.addWidget(self.label)
        right_layout.addWidget(self.progress_label)

        self.start_button.clicked.connect(self.StartButtonPushed)
        self.stop_button.clicked.connect(self.StopButtonPushed)
        self.pause_button.clicked.connect(self.PauseButtonPushed)
        self.ts_button.clicked.connect(self.TsButtonPushed)
        self.cs_button.clicked.connect(self.CsButtonPushed)
        self.ttl_button.clicked.connect(self.TTLButtonPushed)
        self.connect_button.clicked.connect(self.ConnectButtonPushed)
        self.serial_button.clicked.connect(self.SerialButtonPushed)

        # Timer for background tasks
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.runBackgroundTask)
        self.timer.start(100)  # Adjust the interval as needed

    def runBackgroundTask(self):
        # This method runs background tasks without blocking the GUI thread
        pass

    def startButtonPushed(self):
        if not self.isRunning:

                    # Update status
                    self.isRunning = True
                    self.startButton.setStyleSheet("background-color: green")
                    ipi = value of IPI dial
                    numLoops = value of nREP dial
                    iti = value of ITI dial
                    
                    # Send the IPI command
                    self.arduinoSerial.write(f'SET,IPI1,{ipi}'.encode())
                    
                    # stimulation:
                    for i in numLoops:
                      
                      self.arduinoSerial.write(b'START1')
                      wait(iti)
                      progress = (i / numLoops) * 100
                      progressbarwidget(progress)


    def StopButtonPushed(self):
        if self.isRunning:
            self.isRunning = False
            self.stopbutton.setStyleSheet("background-color: red")
            self.startbutton.setStyleSheet("background-color: gray")
            progressbarwidget("0")


    def PauseButtonPushed(self):
        # Update the Lamp status and display a message
        if self.isbreak:
            self.isbreak = False
            self.pausa = False
            print('PLAY')
            self.pause_button.setText('PAUSE')
        elif not self.isbreak:
            self.isbreak = True
            self.pausa = True
            print('PAUSE')
            self.pause_button.setText('PLAY')

    def TsButtonPushed(self):
        try:
            self.arduinoSerial.write(b'SET,test,1\n')
            self.triggercatch.setText('')
        except Exception as e:
            self.triggercatch.setText('!!! Serial is not connected !!!')

    def CsButtonPushed(self):
        try:
            self.arduinoSerial.write(b'SET,test,2\n')
            self.triggercatch.setText('')
        except Exception as e:
            self.triggercatch.setText('!!! Serial is not connected !!!')

    def TTLButtonPushed(self):
        try:
            self.arduinoSerial.write(b'SET,test,3\n')
            self.triggercatch.setText('')
        except Exception as e:
            self.triggercatch.setText('!!! Serial is not connected !!!')

    def ConnectButtonPushed(self):
        # Get the serial port from the QLineEdit
        serial_port = self.serial_edit.text()

        try:
            # Initialize the Arduino serial port using the specified serial_port
            self.arduinoSerial = serial.Serial(serial_port, 115200)

            # Open the serial connection
            self.arduinoSerial.open()

            # Pause to ensure the Arduino is ready
            QTimer.singleShot(2000, lambda: self.serialcatch.setText(' '))

        except Exception as e:
            # If there's an error while opening the serial connection, handle it here
            # For example, you can display an error message or set the lamp color to red.
            self.serialcatch.setText('!!! Serial name is non valid !!!')

    def SerialButtonPushed(self):
        # Automatically detect the Arduino serial port
        ports = [p.device for p in serial.tools.list_ports.comports() if 'Arduino' in p.description]
        if ports:
            self.serial_edit.setText(ports[0])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ppTMSApp()
    window.show()
    sys.exit(app.exec_())
