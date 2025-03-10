from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy, QHBoxLayout
from PyQt5.QtChart import QChart, QPieSeries, QChartView, QChartView, QBarSet, QBarSeries, QBarCategoryAxis
from PyQt5.QtGui import QPainter, QColor

import numpy as np
from datetime import date, timedelta, datetime
from math import log10

class CircleWidget(QWidget):
    def __init__(self, data, title, index, colors = None):
        super().__init__()

        if colors != None:
            self.colors = colors
        self.index = index
        self.data = data
        self.title = title
        self.setGeometry(100, 100, 300, 300)

        layout = QVBoxLayout(self)
        chart_view = self.create_donutchart()
        layout.addWidget(chart_view)

        self.setLayout(layout)

    def create_donutchart(self):
        series = QPieSeries()
        
        chartableData = {i[self.index]:sum([s[-2] for s in self.data if s[self.index] == i[self.index] and s[-2]<0]) for i in self.data}
        series.setHoleSize(0.50)
        for key in list(chartableData.keys()):
            slice = series.append(key, chartableData[key])
            if chartableData[key] != 0:
                slice.setLabelVisible(True)
                try:
                    slice.setColor(QColor(tuple(self.colors[key])[0], tuple(self.colors[key])[1], tuple(self.colors[key])[2]))
                except:
                    pass

        chart = QChart()
        chart.legend().hide()
        chart.addSeries(series)
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTitle(self.title)
        

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)

        return chart_view
    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
                elif child.layout():
                    self.clearLayout(child.layout())

class BarWidget(QWidget):
    def __init__(self, data):
        super().__init__()
        self.setGeometry(100,100, 200, 300)

        self.data = data
        layout = QVBoxLayout(self)
        chart_view = self.create_bar()
        layout.addWidget(chart_view)
        self.setLayout(layout)
        self.show()
        

    def create_bar(self):
        set0 = QBarSet(None)
        set0.setColor(QColor(0, 255, 0))
        set1 = QBarSet(None)
        set1.setColor(QColor(255, 0, 0))
        set0 << sum([i[-2] for i in self.data if i[-2] > 0]) 
        set1 << abs(sum([i[-2] for i in self.data if i[-2] < 0]))

        series = QBarSeries()
        series.append(set0)
        series.append(set1)

        chart = QChart()

        chart.legend().setVisible(False)
        chart.addSeries(series)
        chart.setAnimationOptions(QChart.SeriesAnimations)
        
        categories = ["Zyski/Straty"]
        axis = QBarCategoryAxis() 
        axis.append(categories)
        chart.createDefaultAxes()
        chart.setAxisX(axis, series)

        chartView = QChartView(chart)
        chartView.setRenderHint(QPainter.Antialiasing)

        return chartView

class QInfoWidget(QWidget):
    def __init__(self, data, colors) -> None:
        super().__init__()
        self.data = data
        self.colors = colors
        self.accessibleLayout = QHBoxLayout()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.accessibleLayout.setContentsMargins(0, 0, 0, 0)
        self.accessibleLayout.setSpacing(0)
        self.balanceWidget = BarWidget(self.data)
        self.gainsWidget = CircleWidget(self.data, "Wydatki ze wzgledu na kategorie", 1, colors)
        self.lossesImage = CircleWidget(self.data, "Wydatki ze wzgledu na osoby", 0)
        self.accessibleLayout.addWidget(self.balanceWidget)
        self.accessibleLayout.addWidget(self.gainsWidget)
        self.accessibleLayout.addWidget(self.lossesImage)
        self.setLayout(self.accessibleLayout)

        with open('styleSHEETS/info_stylesheet.qss', 'r') as file:
            style = file.read()
            self.setStyleSheet(style)

    def updateData(self, data) -> None:
        self.gainsWidget.graphData = data
        self.gainsWidget.refreshData() 