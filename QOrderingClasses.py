from PyQt5.QtWidgets import QPushButton, QWidget, QHBoxLayout
from PyQt5.QtCore import pyqtSignal
class QOrderButton(QPushButton):
    changedState = pyqtSignal()
    # a class that will be used for ordering purposses of only one thing
    def __init__(self, name: str, state=0) -> None:
        super().__init__()
        self.setFlat(True)
        self.clicked.connect(self.changeMode)
        self.state = state
        self.graphicsText = [name, f"{name} ASC", f"{name} DESC"]
        self.setText(self.graphicsText[self.state])

    def changeMode(self):
        if self.state < 2:
            self.state += 1
        else:
            self.state = 1
        self.setText(self.graphicsText[self.state])
        self.update()
        self.changedState.emit()

    def reset(self):
        self.state = 0
        self.setText(self.graphicsText[0])
        self.update()

class QOrderBoard(QWidget):
    changedFilter = pyqtSignal()
    # a class for ordering all the data - board of order buttons
    def __init__(self, prevFilter = None) -> None:
        super().__init__()
        self.mainLayout = QHBoxLayout()
        self.filterDict = {0:"people.personName", 1:"categories.name", 2:"transactions.money", 3:"transactions.date"}
        self.reverseFilterDict = {self.filterDict[key]:key for key in list(self.filterDict.keys())}
        if prevFilter == None:
            self.buttons = [QOrderButton(text[0], text[1]) for text in [('Nazwa', 0), ('Kategoria', 0), ('Kwota', 0), ('Data', 1)]]
            self.currentFilter = "transactions.date ASC"
        else:
            self.currentFilter = prevFilter
            prevButtonText = self.currentFilter.split()[0]
            prevButtonFilter = self.currentFilter.split()[1]
            text = [['Nazwa', 0], ['Kategoria', 0], ['Kwota', 0], ['Data', 0]]
            if prevButtonFilter == "ASC":
                text[self.reverseFilterDict[prevButtonText]][1] = 1
            else:
                text[self.reverseFilterDict[prevButtonText]][1] = 2
            self.buttons = [QOrderButton(t[0], t[1]) for t in text]

        self.pastBoardContent = [but.text() for but in self.buttons]
        for but in self.buttons:
            but.changedState.connect(self.reset)
            self.mainLayout.addWidget(but)
        self.setLayout(self.mainLayout)
        with open('styleSHEETS/qorder_stylesheet.qss', 'r') as file:
            style = file.read()
            self.setStyleSheet(style)

    def reset(self):
        if self.pastBoardContent != []:
            changed = [but.text() for but in self.buttons if but.text() not in self.pastBoardContent]
            if len(changed) == 1:
                if changed[0][-4:] == "DESC" or changed[0][-4:] == " ASC":
                    self.currentFilter = self.filterDict[[but.text() for but in self.buttons].index(changed[0])] + ' ' + changed[0][-4:]
                else:
                    self.currentFilter = "transactions.date DESC"
                for but in self.buttons:
                    if but.text() != changed[0]:
                        but.reset()
            self.pastBoardContent = [but.text() for but in self.buttons]
            self.update()
        else:
            self.pastBoardContent = [but.text() for but in self.buttons]
        self.changedFilter.emit()