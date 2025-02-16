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
        with open('styleSHEETS/info_stylesheet.qss', 'r') as file:
            style = file.read()
            self.setStyleSheet(style)
        self.graphData = data
        layout = QVBoxLayout(self)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        self.figure.tight_layout()
        self.setLayout(layout)
        self.plot()

    def plot(self) -> None:
        plt.style.use('dark_background')
        fig, ax = plt.subplots()
        x = [date(int(i[-1][0:4]), int(i[-1][5:7]), int(i[-1][8:])) for i in self.graphData]
        y = [sum([i[-2] for i in self.graphData if i[-1] == j]) for j in [k.strftime("%Y-%m-%d") for k in x]]
        colors = [(1, 0, 0) if i<0 else (0, 1, 0) for i in y]
        ax = self.figure.add_subplot(111)
        
        barplot = ax.bar(x, y, width=0.1, color=colors)
        label_step = (max(y) - min(y)) / 20
        labels = [int(min(y) + i * label_step) for i in range(20)]

        # Add labels to the bars
        ax.bar_label(barplot, labels=labels[:len(barplot)], label_type="edge")
        ax.set(adjustable='box', ylim=(min(y)-100, max(y)+100))
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
       