from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QSizePolicy, QHBoxLayout, QButtonGroup, QStackedWidget, QPushButton, QCheckBox
from fundamentalClasses import SQL_SINGLE_INSTANCE
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np


class MatplotlibWidget(QWidget):
    def __init__(self, data, plotType):
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

    def clear_layout(self, layout):
        self.prevVariables = []
        if layout is not None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget() is not None:
                    if not isinstance(child.widget(), QPushButton):
                        try:
                            self.prevVariables.append(child.widget().text())
                        except:
                            self.prevVariables.append(child.widget().date())
                    child.widget().deleteLater()
                elif child.layout() is not None:
                    self.clear_layout(child.layout())
    
class NavigationSettingsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.accessibleLayout = QVBoxLayout()
        self.buttonLayout = QHBoxLayout()
        self.buttonWidget = QWidget()
        self.currentGraph = 'Kategorie'
        self.balanceCheckBox = QCheckBox('saldo wypadkowe (SW)')
        self.medianCheckBox = QCheckBox('prosta mediany')
        self.avgCheckBox = QCheckBox('prosta średniej')

        self.balanceCheckBox.setChecked(False)
        self.medianCheckBox.setChecked(False)
        self.avgCheckBox.setChecked(False)
        self.setButtonProperties()

        self.accessibleLayout.addWidget(self.buttonWidget)
        self.accessibleLayout.addWidget(self.balanceCheckBox)
        self.accessibleLayout.addWidget(self.medianCheckBox)
        self.accessibleLayout.addWidget(self.avgCheckBox)
        self.accessibleLayout.setContentsMargins(0, 0, 0, 0)
        self.accessibleLayout.setSpacing(0)
        self.setLayout(self.accessibleLayout)


    

    def setButtonProperties(self) -> None:
        self.buttonObjList = []
        self.buttonGroup = QButtonGroup(self)
        self.buttonGroup.buttonToggled.connect(self.refreshData)
        self.buttonGroup.setExclusive(True)
        for i in 'Kategorie', 'Osoby', 'Czas':
            self.buttonObjList.append(QPushButton(i, self))
            self.buttonGroup.addButton(self.buttonObjList[-1])
            self.buttonObjList[-1].setObjectName('buttonListItem')
            self.buttonObjList[-1].setCheckable(True)
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
        self.plotImage = MatplotlibWidget(data, currentPlotType)
        self.navWidget = NavigationSettingsWidget()
        self.accessibleLayout.addWidget(self.navWidget)
        self.accessibleLayout.addWidget(self.plotImage)
        self.setLayout(self.accessibleLayout)
        with open('styleSHEETS/info_stylesheet.qss', 'r') as file:
            style = file.read()
            self.setStyleSheet(style)

    
    def updateData(self, data) -> None:
        pass
       