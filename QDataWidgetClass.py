from fundamentalClasses import SQL_DATA_HANDLE
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QLineEdit

class QDataWidget(QWidget):
    def __init__(self, variables: list, colors: list) -> None:
        super().__init__()
        self.readLayout = QHBoxLayout()
        self.currentIndex = 0
        self.widgetList = [[], []]
        self.variables = variables
        self.colors = colors

        self.populateLine()
        self.setLayout(self.readLayout)

    def populateLine(self):
        for x in self.variables:
            self.widgetList[0].append(QLabel(str(x)))
            self.widgetList[1].append(QLineEdit(str(x)))
            if self.variables.index(x) == 1:
                self.widgetList[0][-1].setStyleSheet(f"color: rgb({self.colors[0]}, {self.colors[1]}, {self.colors[2]});")
            if self.variables.index(x) == 2:
                if x == abs(x):
                    self.widgetList[0][-1].setStyleSheet("color: rgb(0, 255, 0);")
                else:
                    self.widgetList[0][-1] = QLabel('-' + str(x))
                    self.widgetList[1][-1] = QLineEdit('-' + str(x))
                    self.widgetList[0][-1].setStyleSheet("color: rgb(255, 0, 0)")
        self.widgetList[0].append(QPushButton("Edycja"))
        self.widgetList[0][-1].clicked.connect(self.changeLayout)
        self.widgetList[1].append(QPushButton("Zapisz zmiany"))
        self.widgetList[1][-1].clicked.connect(self.changeLayout)
        for widg in self.widgetList[self.currentIndex]:
            self.readLayout.addWidget(widg)

    def changeLayout(self):
        self.clear_layout(self.layout())
        self.currentIndex = not self.currentIndex
        self.populateLine()
        self.setLayout(self.readLayout)
        self.update()
    
    def clear_layout(self, layout):
        if layout is not None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget() is not None:
                    child.widget().deleteLater()
                elif child.layout() is not None:
                    self.clear_layout(child.layout())