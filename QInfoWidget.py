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
        self.bGroup = QButtonGroup()
        self.buttonWidget = QWidget()
        self.buttonlayout = QHBoxLayout()
        self.stackedWidget = QStackedWidget()
        for i in range(10):
            button = QPushButton(f'Test {i}')
            button.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(i))
            self.buttonlayout.addWidget(button)
            self.bGroup.addButton(button)
            self.stackedWidget.addWidget(QLabel(f'Test {i}'))
        
        self.buttonWidget.setLayout(self.buttonlayout)
        self.accessibleLayout.addWidget(self.buttonWidget)
        self.accessibleLayout.addWidget(self.stackedWidget)
        self.setLayout(self.accessibleLayout)



class QInfoWidget(QWidget):
    def __init__(self, data, currentPlotType) -> None:
        super().__init__()
        self.accessibleLayout = QVBoxLayout()
        self.data = data
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.accessibleLayout.setContentsMargins(0, 0, 0, 0)
        self.accessibleLayout.setSpacing(0)
        self.plotImage = MatplotlibWidget()
        self.accessibleLayout.addWidget(self.plotImage)
        self.accessibleLayout.addWidget(NavigationSettingsWidget())
        self.setLayout(self.accessibleLayout)
       