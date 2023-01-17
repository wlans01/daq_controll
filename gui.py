import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QSlider, QVBoxLayout, QWidget

class SlidersWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Create two sliders
        self.slider1 = QSlider(Qt.Horizontal)
        self.slider2 = QSlider(Qt.Horizontal)

        # Set the range for both sliders
        self.slider1.setRange(-10, 10)
        self.slider2.setRange(-10, 10)

        # Create labels for the sliders
        self.label1 = QLabel('0')
        self.label2 = QLabel('0')

        # Connect the valueChanged signal of the sliders to the updateLabel method
        self.slider1.valueChanged.connect(self.updateLabel1)
        self.slider2.valueChanged.connect(self.updateLabel2)

        # Add scale to the sliders
        self.slider1.setTickPosition(QSlider.TicksBelow)
        self.slider1.setTickInterval(1)
        self.slider2.setTickPosition(QSlider.TicksBelow)
        self.slider2.setTickInterval(1)

        # Create a layout to hold the first slider, label and scale
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.slider1)
        hbox1.addWidget(self.label1)

        # Create a layout to hold the second slider, label and scale
        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.slider2)
        hbox2.addWidget(self.label2)

        # Create a vertical layout to hold the two horizontal layouts
        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)

        # Set the layout for the widget
        self.setLayout(vbox)

        # Set the window
       # Set the window properties
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Sliders')
        self.show()

    # Method to update the label when the value of the slider changes
    def updateLabel1(self, value):
        self.label1.setText(str(value))

    def updateLabel2(self, value):
        self.label2.setText(str(value))
        self.slider2.setTickPosition(QSlider.TicksBelow)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SlidersWindow()
    sys.exit(app.exec_())