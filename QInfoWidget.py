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
        self.buttonWidget = QWidget()
        self.stackedWidget = QStackedWidget()

        self.createView1()
        self.createView2()
        self.createView3()
        self.setButtonProperties()

        self.accessibleLayout.addWidget(self.buttonWidget)
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

    def setButtonProperties(self) -> None:
        self.buttonObjList = []
        self.buttonGroup = QButtonGroup(self)
        self.buttonGroup.buttonToggled.connect(self.refreshData)
        self.buttonGroup.setExclusive(True)
        for i in [('Kategorie', lambda: self.stackedWidget.setCurrentIndex(0)),
                   ('Osoby', lambda: self.stackedWidget.setCurrentIndex(1)), 
                   ('Czas', lambda: self.stackedWidget.setCurrentIndex(2))]:
            self.buttonObjList.append(QPushButton(i[0], self))
            self.buttonGroup.addButton(self.buttonObjList[-1])
            self.buttonObjList[-1].setObjectName('buttonListItem')
            self.buttonObjList[-1].setCheckable(True)
            self.buttonObjList[-1].clicked.connect(i[1])
            self.buttonLayout.addWidget(self.buttonObjList[-1])

        self.buttonLayout.setSpacing(0)
        self.buttonLayout.setContentsMargins(0, 0, 0, 0)

        self.buttonWidget.setLayout(self.buttonLayout)
        self.buttonWidget.setObjectName('buttonWidg')

    def refreshData(self):
        pass

class QInfoWidget(QWidget):
    def __init__(self, data, currentPlotType) -> None:
        super().__init__()
        self.accessibleLayout = QVBoxLayout()
        self.data = data
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.accessibleLayout.setContentsMargins(0, 0, 0, 0)
        self.accessibleLayout.setSpacing(0)
        self.plotImage = MatplotlibWidget()
        self.navWidget = NavigationSettingsWidget()
        self.accessibleLayout.addWidget(self.navWidget)
        self.accessibleLayout.addWidget(self.plotImage)
        self.setLayout(self.accessibleLayout)
        with open('styleSHEETS/info_stylesheet.qss', 'r') as file:
            style = file.read()
            self.setStyleSheet(style)

    
    def updateData(self, data) -> None:
        pass
       