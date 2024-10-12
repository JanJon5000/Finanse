from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout


class QInfoWidget(QWidget):
    def __init__(self, data) -> None:
        super().__init__()
        self.accessibleLayout = QGridLayout()
        self.data = data
        self.populateLayout()

    def populateLayout(self):
        self.balanceWidget = QLabel("test")
        self.dataWidgets = {
            'infoTexts':[QLabel("srednie zyski/straty:"), QLabel("najmniejszy/największy zysk/strata w jednej transakcji"), QLabel('mediana zysków/strat'), QLabel('udzial kategorii w zyskach/stratach'), QLabel('udzial osób w zyskach/stratach')],
            'incomeWidgets':[QLabel("test0"), QLabel("test1"), QLabel("test2"), QLabel("test3"), QLabel("test4")],
            'spendingsWidgets':[QLabel("test0"), QLabel("test1"), QLabel("test2"), QLabel("test3"), QLabel("test4")]
        }
        self.accessibleLayout.addWidget(self.balanceWidget, 0, 0, 1, 3)
        columnCounter = 0
        for l in [self.dataWidgets['infoTexts'], self.dataWidgets['incomeWidgets'], self.dataWidgets['spendingsWidgets']]:
            for w in l:
                self.accessibleLayout.addWidget(w, l.index(w)+1, columnCounter)
            columnCounter += 1
        self.setLayout(self.accessibleLayout)
    
    def updateData(self, data):
        self.data = data
        for comm in [["self.balanceWidget.setText(str(sum([tpl[2] for tpl in self.data])))", "self.balanceWidget.setText('0')"],
                     ["self.dataWidgets['incomeWidgets'][0].setText(f'{round(sum([tpl[2] for tpl in self.data if tpl[2] >= 0])/len([tpl[2] for tpl in self.data if tpl[2] >= 0]), 2)}')", "self.dataWidgets['incomeWidgets'][0].setText('0')"],
                     ["self.dataWidgets['spendingsWidgets'][0].setText(f'{round(sum([tpl[2] for tpl in self.data if tpl[2] <= 0])/len([tpl[2] for tpl in self.data if tpl[2] <= 0]), 2)}')", "self.dataWidgets['spendingsWidgets'][0].setText('0')"],
                     ["self.dataWidgets['incomeWidgets'][1].setText(f'{max([tpl[2] for tpl in self.data if tpl[2] >= 0])} / {min([tpl[2] for tpl in self.data if tpl[2] >= 0])}')", "self.dataWidgets['incomeWidgets'][1].setText('0/0')"],
                     ["self.dataWidgets['spendingsWidgets'][1].setText(f'{max([tpl[2] for tpl in self.data if tpl[2] <= 0])} / {min([tpl[2] for tpl in self.data if tpl[2] <= 0])}')", "self.dataWidgets['spendingsWidgets'][1].setText('0/0')"]
                     ]:
            try:
                exec(comm[0])
            except:
                exec(comm[1])