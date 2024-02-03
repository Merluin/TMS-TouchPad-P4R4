import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QSlider, QLabel, QPushButton

class ppTMSApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        # Vertical layout for the entire app
        v_layout = QVBoxLayout()

        # Horizontal layout for parameters and ppTMS
        h_layout_params = QHBoxLayout()
        v_layout_params = QVBoxLayout()
        h_layout_ppTMS = QHBoxLayout()

        # Creating sliders
        self.slider_ipi = QSlider()
        self.slider_rep = QSlider()
        self.slider_itl = QSlider()

        # Slider labels
        label_ipi = QLabel('IPI')
        label_rep = QLabel('Rep')
        label_itl = QLabel('ITI')

        # Adding sliders and labels to the layout
        v_layout_params.addWidget(label_ipi)
        v_layout_params.addWidget(self.slider_ipi)
        v_layout_params.addWidget(label_rep)
        v_layout_params.addWidget(self.slider_rep)
        v_layout_params.addWidget(label_itl)
        v_layout_params.addWidget(self.slider_itl)

        # Creating buttons
        self.btn_ts = QPushButton('TS')
        self.btn_cs = QPushButton('CS')
        self.btn_bio = QPushButton('Bio')

        # Adding buttons to the layout
        v_layout_params.addWidget(self.btn_ts)
        v_layout_params.addWidget(self.btn_cs)
        v_layout_params.addWidget(self.btn_bio)

        # Creating ppTMS label and buttons
        self.label_ppTMS = QLabel('ppTMS\n0%')
        self.btn_start = QPushButton('START')
        self.btn_pause = QPushButton('PAUSE')
        self.btn_stop = QPushButton('STOP')

        # Adding ppTMS label and buttons to the layout
        h_layout_ppTMS.addWidget(self.label_ppTMS)
        h_layout_ppTMS.addWidget(self.btn_start)
        h_layout_ppTMS.addWidget(self.btn_pause)
        h_layout_ppTMS.addWidget(self.btn_stop)

        # Adding sublayouts to the main layout
        h_layout_params.addLayout(v_layout_params)
        h_layout_params.addLayout(h_layout_ppTMS)
        v_layout.addLayout(h_layout_params)

        # Set the main layout to the window
        self.setLayout(v_layout)

        # Window title
        self.setWindowTitle('ppTMS App')

        # Window dimensions
        self.setGeometry(300, 300, 600, 300)

def main():
    app = QApplication(sys.argv)
    ex = ppTMSApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
