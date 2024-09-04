from fundamentalClasses import SQL_DATA_HANDLE
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton

class QDataWidget(QWidget):
    def __init__(self, variables: list, colors: list) -> None:
        super().__init__()
        self.accessibleLayout = QHBoxLayout()
        self.widgetList = []
        self.textList = []
        for x in variables:
            self.widgetList.append(QLabel(str(x)))
            self.textList.append(str(x))
            if variables.index(x) == 1:
                self.widgetList[-1].setStyleSheet(f"color: rgb({colors[0]}, {colors[1]}, {colors[2]});")
            if variables.index(x) == 2:
                if x == abs(x):
                    self.widgetList[-1].setStyleSheet("color: rgb(0, 255, 0);")
                else:
                    self.widgetList[-1] = QLabel('-' + str(x), self)
                    self.widgetList[-1].setStyleSheet("color: rgb(255, 0, 0)")
            self.accessibleLayout.addWidget(self.widgetList[-1])
        self.widgetList.append(QPushButton("Usuń"))
        self.accessibleLayout.addWidget(self.widgetList[-1])
        self.setLayout(self.accessibleLayout)
