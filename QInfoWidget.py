from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QVBoxLayout, QListWidget, QScrollArea, QSizePolicy, QHBoxLayout, QTreeWidget
from fundamentalClasses import SQL_SINGLE_INSTANCE

class QParticipationWidget(QWidget):
    def __init__(self, keyword, num) -> None:
        super().__init__()
        self.getData(keyword=keyword, num=num)
        self.accesibleLayout = QVBoxLayout()
        self.listComponent = QTreeWidget()
        self.listComponent.setSelectionMode(QTreeWidget.NoSelection)
        self.listComponent.setColumnCount(2)
        self.listComponent.setHeaderHidden(True)
        self.listComponent.setRootIsDecorated(False)

        self.scrollWidget = QScrollArea()
        self.scrollWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollWidget.setWidget(self.listComponent)
        self.accesibleLayout.addWidget(self.scrollWidget)
        self.setLayout(self.accesibleLayout)

class QInfoWidget(QWidget):
    def __init__(self, data) -> None:
        super().__init__()
        self.accessibleLayout = QGridLayout()
        self.data = data
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.populateLayout()

    def populateLayout(self) -> None:
        self.balanceWidget = QLabel("test")
        self.dataWidgets = {
            'infoTexts':[QLabel("średnia"), QLabel("max/min"), QLabel('mediana'), QLabel('udzial kategorii'), QLabel('udzial osób')],
            'incomeWidgets':[QLabel("test0"), QLabel("test1"), QLabel("test2"), QParticipationWidget('name', 1), QParticipationWidget('personName', 1)],
            'spendingsWidgets':[QLabel("test0"), QLabel("test1"), QLabel("test2"), QParticipationWidget('name', -1), QParticipationWidget('personName', -1)]
        }
        self.combineWidgets = [[QWidget(), QHBoxLayout()], [QWidget(), QHBoxLayout()], [QWidget(), QHBoxLayout()], [QWidget(), QGridLayout()], [QWidget(), QGridLayout()]]
        self.accessibleLayout.addWidget(self.balanceWidget, 0, 0, 1, 3)
        columnCounter = 0
        for l in [self.dataWidgets['infoTexts'], self.dataWidgets['incomeWidgets'], self.dataWidgets['spendingsWidgets']]: 
            for w in l:
                self.accessibleLayout.addWidget(w, l.index(w)+1, columnCounter)
            columnCounter += 1
        self.setWidgetProperties()
        self.setLayout(self.accessibleLayout)
    
    def updateData(self, data) -> None:
        self.data = data
        for comm in [["self.balanceWidget.setText(str(sum([tpl[2] for tpl in self.data])))", "self.balanceWidget.setText('0')"],
                     ["self.dataWidgets['incomeWidgets'][0].setText(f'{round(sum([tpl[2] for tpl in self.data if tpl[2] >= 0])/len([tpl[2] for tpl in self.data if tpl[2] >= 0]), 2)}')", "self.dataWidgets['incomeWidgets'][0].setText('0')"],
                     ["self.dataWidgets['spendingsWidgets'][0].setText(f'{round(sum([tpl[2] for tpl in self.data if tpl[2] <= 0])/len([tpl[2] for tpl in self.data if tpl[2] <= 0]), 2)}')", "self.dataWidgets['spendingsWidgets'][0].setText('0')"],
                     ["self.dataWidgets['incomeWidgets'][1].setText(f'{max([tpl[2] for tpl in self.data if tpl[2] >= 0])} / {min([tpl[2] for tpl in self.data if tpl[2] >= 0])}')", "self.dataWidgets['incomeWidgets'][1].setText('0/0')"],
                     ["self.dataWidgets['spendingsWidgets'][1].setText(f'{min([tpl[2] for tpl in self.data if tpl[2] <= 0])} / {max([tpl[2] for tpl in self.data if tpl[2] <= 0])}')", "self.dataWidgets['spendingsWidgets'][1].setText('0/0')"],
                     ['self.dataWidgets["incomeWidgets"][2].setText(f"{sorted([tpl[2] for tpl in self.data if tpl[2] >= 0])[int(len([tpl[2] for tpl in self.data if tpl[2] >= 0])/2)]}")','self.dataWidgets["incomeWidgets"][2].setText("0")'],
                     ['self.dataWidgets["spendingsWidgets"][2].setText(f"{sorted([tpl[2] for tpl in self.data if tpl[2] <= 0])[int(len([tpl[2] for tpl in self.data if tpl[2] <= 0])/2)]}")','self.dataWidgets["spendingsWidgets"][2].setText("0")']
                     ]:
            try:
                exec(comm[0])
            except:
                exec(comm[1])
    
    def fillLists(self) -> None:
        if self.data != []:
            for widg in [self.dataWidgets['incomeWidgets'][-1], self.dataWidgets['incomeWidgets'][-2], self.dataWidgets['spendingsWidgets'][-1], self.dataWidgets['spendingsWidgets'][-2]]:
                pass

    def setWidgetProperties(self) -> None:
        for w in self.dataWidgets['incomeWidgets']:
            w.setStyleSheet('color: GREEN;')
            w.setObjectName('infotext')
            w.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        for w in self.dataWidgets['spendingsWidgets']:
            w.setStyleSheet('color: RED;')
            w.setObjectName('infotext')
            w.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        for w in self.dataWidgets['infoTexts']:
            w.setObjectName('infotext')
            w.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        with open('styleSHEETS/info_stylesheet.qss', 'r') as file:
            style = file.read()
            self.setStyleSheet(style)
        