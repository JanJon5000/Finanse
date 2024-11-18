from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QSizePolicy, QHBoxLayout, QButtonGroup, QStackedWidget, QPushButton
from fundamentalClasses import SQL_SINGLE_INSTANCE
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np


class MatplotlibWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        self.figure.tight_layout()
        self.setLayout(layout)
        self.plot()

    def plot(self):
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        ax = self.figure.add_subplot(111)
        ax.plot(x, y)
        self.canvas.draw()

class NavigationSettingsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.accessibleLayout = QVBoxLayout()
        self.buttonLayout = QHBoxLayout()
        self.stackedWidget = QStackedWidget()

        self.createView1()
        self.createView2()
        self.createView3()

        
        button = QPushButton(f'test 1', self)
        button.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.buttonLayout.addWidget(button)

        button2 = QPushButton(f'test 2', self)
        button2.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.buttonLayout.addWidget(button2)

        button3 = QPushButton(f'test 3', self)
        button3.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.buttonLayout.addWidget(button3)

        self.accessibleLayout.addLayout(self.buttonLayout)
        self.accessibleLayout.addWidget(self.stackedWidget)

        self.setLayout(self.accessibleLayout)

    def createView1(self):
        view = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel('Test 1', self))
        view.setLayout(layout)

        self.stackedWidget.addWidget(view)

    def createView2(self):
        view = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel('Test 2', self))
        view.setLayout(layout)

        self.stackedWidget.addWidget(view)

    def createView3(self):
        view = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel('Test 3', self))
        view.setLayout(layout)

        self.stackedWidget.addWidget(view)



class QInfoWidget(QWidget):
    def __init__(self, data, currentPlotType) -> None:
        super().__init__()
        self.accessibleLayout = QVBoxLayout()
        self.data = data
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.accessibleLayout.setContentsMargins(0, 0, 0, 0)
        self.accessibleLayout.setSpacing(0)
        self.plotImage = MatplotlibWidget()
        self.accessibleLayout.addWidget(NavigationSettingsWidget())
        self.accessibleLayout.addWidget(self.plotImage)
        self.setLayout(self.accessibleLayout)
       