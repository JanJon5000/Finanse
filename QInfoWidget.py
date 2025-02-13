from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QSizePolicy, QHBoxLayout, QButtonGroup, QStackedWidget, QPushButton, QCheckBox
from fundamentalClasses import SQL_SINGLE_INSTANCE
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from datetime import date, timedelta, datetime

class MatplotlibWidget(QWidget):
    def __init__(self, data) -> None:
        super().__init__()
        self.graphData = data
        layout = QVBoxLayout(self)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        self.figure.tight_layout()
        self.setLayout(layout)
        self.plot()

    def plot(self) -> None:
        print(self.graphData)
        plt.style.use('dark_background')
        fig, ax = plt.subplots()
        x = [date(2010, 12, 1),
            date(2011, 1, 4),
            date(2012, 1, 4),
            date(2011, 9, 4),
            date(2011, 8, 4),
            date(2011, 7, 4),
            date(2011, 6, 4),
            date(2011, 5, 5)]
        y = [4.8, -5.5, -3.5, 4.6, -6.5, 6.6, 2.6, 3.0]
        colors = [(1, 0, 0) if i<0 else (0, 1, 0) for i in y]
        ax = self.figure.add_subplot(111)
        
        ax.bar(x, y, width=2, color=colors, edgecolor="white", linewidth=0.4)
        ax.set(adjustable='box', ylim=(-9, 8), yticks=np.arange(-10, 8))
        ax.xaxis_date()
        self.canvas.draw()



    def clearLayout(self, layout):
        self.prevVariables = []
        if layout is not None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget() is not None:
                    child.widget().deleteLater()
                elif child.layout() is not None:
                    self.clear_layout(child.layout())
    
    def refreshData(self):
        pass

class QInfoWidget(QWidget):
    def __init__(self, data) -> None:
        super().__init__()
        self.accessibleLayout = QVBoxLayout()
        self.data = data
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.accessibleLayout.setContentsMargins(0, 0, 0, 0)
        self.accessibleLayout.setSpacing(0)
        self.plotImage = MatplotlibWidget(data)
        self.accessibleLayout.addWidget(self.plotImage)
        self.setLayout(self.accessibleLayout)
        with open('styleSHEETS/info_stylesheet.qss', 'r') as file:
            style = file.read()
            self.setStyleSheet(style)

    
    def updateData(self, data) -> None:
        pass
       