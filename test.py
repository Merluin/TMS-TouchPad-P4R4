import sys
from PyQt5 import QtWidgets

class ExampleApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('PyQt5 Simple Test')
        self.setGeometry(100, 100, 280, 80)
        self.show()

def main():
    app = QtWidgets.QApplication(sys.argv)
    ex = ExampleApp()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
