from fundamentalClasses import SQL_DATA_HANDLE
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QLineEdit

class QDataWidget(QWidget):
    def __init__(self, variables: list, colors: list) -> None:
        super().__init__()
        self.readLayout = QHBoxLayout()
        self.currentIndex = 0
        self.variables = variables
        self.prevVariables = variables
        self.colors = colors

        self.populateLine()
        self.setLayout(self.readLayout)

    def populateLine(self):
        if self.currentIndex == 0:
            for x in self.variables:
                x = QLabel(str(x))
                try: 
                    if self.variables.index(x.text()) == 1:
                        x.setStyleSheet(f"color: rgb({self.colors[0]}, {self.colors[1]}, {self.colors[2]});")
                    if self.variables.index(x.text()) == 2:
                        if float(x.text()) == abs(float(x.text())):
                            x.setStyleSheet("color: rgb(0, 255, 0);")
                        else:
                            x = QLabel('-' + x.text())
                            x.setStyleSheet("color: rgb(255, 0, 0);")
                except:
                    if self.variables.index(float(x.text())) == 1:
                        x.setStyleSheet(f"color: rgb({self.colors[0]}, {self.colors[1]}, {self.colors[2]});")
                    if self.variables.index(float(x.text())) == 2:
                        if float(x.text()) == abs(float(x.text())):
                            x.setStyleSheet("color: rgb(0, 255, 0);")
                        else:
                            x = QLabel('-' + x.text())
                            x.setStyleSheet("color: rgb(255, 0, 0);")
                self.readLayout.addWidget(x)
            x = QPushButton("Edycja")
            x.clicked.connect(self.changeLayout)
            self.readLayout.addWidget(x)
        elif self.currentIndex == 1:
            for x in self.variables:
                x = QLineEdit(str(x))
                try:
                    if self.variables.index(x.text()) == 2:
                        if float(x.text()) == abs(float(x.text())):
                            pass
                        else:
                            x = QLineEdit('-' + x.text())
                except:
                    if self.variables.index(float(x.text())) == 2:
                        if float(x.text()) == abs(float(x.text())):
                            pass
                        else:
                            x = QLineEdit('-' + x.text())
                self.readLayout.addWidget(x)
            x = QPushButton("Zapisz zmiany")
            x.clicked.connect(self.changeLayout)
            self.readLayout.addWidget(x)

    def changeLayout(self):
        self.clear_layout(self.layout())
        self.currentIndex = not self.currentIndex
        self.populateLine()
        self.update()

    def clear_layout(self, layout):
        if layout is not None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget() is not None:
                    if not isinstance(child.widget(), QPushButton):
                        print(child.widget().text())
                    child.widget().deleteLater()
                elif child.layout() is not None:
                    self.clear_layout(child.layout())