import sys
import serial
from PyQt5 import QtWidgets

class SerialApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize the serial connection
        self.serial = serial.Serial()
        self.serial.baudrate = 9600
        self.serial.timeout = 1

        # Create a button for sending '1' to Arduino
        self.send_button = QtWidgets.QPushButton('Send 1 to Arduino', self)
        self.send_button.clicked.connect(self.send_to_arduino)
        self.send_button.resize(200, 50)
        self.send_button.move(50, 50)  # Move it to an appropriate location in your window

        # Set the size of the window
        self.setGeometry(100, 100, 800, 400)
        self.setWindowTitle('Serial Communication App')

    def send_to_arduino(self):
        port = '/dev/ttyS0'  # Replace with the correct port
        try:
            if not self.serial.is_open:
                self.serial.port = port
                self.serial.open()

            self.serial.write(b'1')
            print("Sent '1' to Arduino")
        except serial.SerialException as e:
            print(f"Error sending to Arduino: {e}")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWin = SerialApp()
    mainWin.show()
    sys.exit(app.exec_())
