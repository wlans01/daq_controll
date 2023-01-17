# from daq_controller import DAQControl
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QLabel, QHBoxLayout, QVBoxLayout, QGraphicsView,QWidget
import pyqtgraph as pg
import sys

class StreamThread(QThread):
    new_data = pyqtSignal(np.ndarray)

    def __init__(self, daq):
        QThread.__init__(self)
        self.daq = daq

    def run(self):
        self.daq.start()
        while True:
            data = self.daq.read()
            self.new_data.emit(data)

class DAQControlGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        # self.daq = DAQControl('Dev1')
        self.init_ui()

    def init_ui(self):
        self.setGeometry(50, 50, 800, 600)
        self.setWindowTitle("DAQ Control")

        # Input channel widgets
        input_channel_label = QLabel("Input Channel:")
        self.input_channel_lineedit = QLineEdit()
        input_channel_button = QPushButton("Add")
        input_channel_button.clicked.connect(self.add_input_channel)
        input_channel_layout = QHBoxLayout()
        input_channel_layout.addWidget(input_channel_label)
        input_channel_layout.addWidget(self.input_channel_lineedit)
        input_channel_layout.addWidget(input_channel_button)

        # Output channel widgets
        output_channel_label = QLabel("Output Channel:")
        self.output_channel_lineedit = QLineEdit()
        output_channel_button = QPushButton("Add")
        output_channel_button.clicked.connect(self.add_output_channel)
        output_channel_layout = QHBoxLayout()
        output_channel_layout.addWidget(output_channel_label)
        output_channel_layout.addWidget(self.output_channel_lineedit)
        output_channel_layout.addWidget(output_channel_button)

        # Start and stop buttons
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_streaming)
        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_streaming)
        self.stop_button.setEnabled(False)
        control_button_layout = QHBoxLayout()
        control_button_layout.addWidget(self.start_button)
        control_button_layout.addWidget(self.stop_button)

            # Create the graph view
        self.graph_widget = pg.GraphicsView()
        self.graph_widget.setBackground('w')
        self.graph_widget.setYRange(-10, 10)
        self.graph_widget.setXRange(0, 100)
        self.graph_widget.setLabel('left', 'Voltage', 'V')
        self.graph_widget.setLabel('bottom', 'Samples')
        self.graph_widget.setTitle("Analog Input")
        self.graph_widget.showGrid(x=True, y=True)
        self.graph_plot = self.graph_widget.plot()

        # Set up the layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(input_channel_layout)
        main_layout.addLayout(output_channel_layout)
        main_layout.addLayout(control_button_layout)
        main_layout.addWidget(self.graph_widget)
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Create thread and connect signals
        self.stream_thread = StreamThread(self.daq)
        self.stream_thread.new_data.connect(self.update_graph)

    def add_input_channel(self):
        channel = self.input_channel_lineedit.text()
        self.daq.add_input_channel(channel)
        self.input_channel_lineedit.clear()

    def add_output_channel(self):
        channel = self.output_channel_lineedit.text()
        self.daq.add_output_channel(channel)
        self.output_channel_lineedit.clear()

    def start_streaming(self):
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.stream_thread.start()

    def stop_streaming(self):
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.stream_thread.quit()

    def update_graph(self, data):
        self.graph_plot.setData(data)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    daq_control = DAQControlGUI()
    daq_control.show()
    sys.exit(app.exec_())