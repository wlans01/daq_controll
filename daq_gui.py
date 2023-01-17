from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,QWidget
import sys
# from daq_controller import DAQControl

class DAQControlGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create DAQControl object
        # self.daq = DAQControl('Dev1')

        # Set window properties
        self.setWindowTitle('DAQ Control')
        self.setGeometry(100, 100, 300, 200)

        # Create widgets
        self.add_input_channel_button = QPushButton('Add Input Channel', self)
        self.add_output_channel_button = QPushButton('Add Output Channel', self)
        self.start_button = QPushButton('Start', self)
        self.stop_button = QPushButton('Stop', self)
        self.input_channel_label = QLabel('Input Channel:', self)
        self.input_channel_lineedit = QLineEdit(self)
        self.output_channel_label = QLabel('Output Channel:', self)
        self.output_channel_lineedit = QLineEdit(self)

        # Create layouts
        self.main_layout = QVBoxLayout()
        self.input_layout = QHBoxLayout()
        self.output_layout = QHBoxLayout()

        # Add widgets to layouts
        self.input_layout.addWidget(self.input_channel_label)
        self.input_layout.addWidget(self.input_channel_lineedit)
        self.input_layout.addWidget(self.add_input_channel_button)
        self.output_layout.addWidget(self.output_channel_label)
        self.output_layout.addWidget(self.output_channel_lineedit)
        self.output_layout.addWidget(self.add_output_channel_button)
        self.main_layout.addLayout(self.input_layout)
        self.main_layout.addLayout(self.output_layout)
        self.main_layout.addWidget(self.start_button)
        self.main_layout.addWidget(self.stop_button)

        # Create central widget and set layout
        self.central_widget = QWidget(self)
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

        # Connect buttons to functions
        self.add_input_channel_button.clicked.connect(self.add_input_channel)
        self.add_output_channel_button.clicked.connect(self.add_output_channel)
        self.start_button.clicked.connect(self.start)
        self.stop_button.clicked.connect(self.stop)

    def add_input_channel(self):
        channel = self.input_channel_lineedit.text()
        self.daq.add_input_channel(channel)

    def add_output_channel(self):
        channel = self.output_channel_lineedit.text()
        self.daq.add_output_channel(channel)

    def start(self):
        self.daq.start()

    def stop(self):
        self.daq.stop()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    daq_control = DAQControlGUI()
    daq_control.show()
    sys.exit(app.exec_())