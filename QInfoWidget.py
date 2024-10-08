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
        self.accessibleLayout.addWidget(self.balanceWidget, 0, 0)
        self.infoTexts = [QLabel("srednie zyski/straty:"), QLabel("maks zyski/straty:")]
        self.incomeWidgets = [QLabel("test0"), QLabel("test")]
        self.spendingsWidgets = [QLabel("test0"), QLabel("test")]
        columnCounter = 0
        for l in [self.infoTexts, self.incomeWidgets, self.spendingsWidgets]:
            for w in l:
                self.accessibleLayout.addWidget(w, l.index(w)+1, columnCounter)
            columnCounter += 1
        self.setLayout(self.accessibleLayout)

    def refresh(self):
        pass

    def clear_layout(self, layout):
        if layout is not None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget() is not None:
                    child.widget().deleteLater()
                elif child.layout() is not None:
                    self.clear_layout(child.layout())
    
    def updateData(self, data):
        self.data = data
        # try:
        #     self.balanceWidget.setText(str(sum([tpl[2] for tpl in self.data])))
        # except:
        #     self.balanceWidget.setText('0')

        # self.incomeWidgets[0].setText(str(sum([tpl[2] for tpl in self.data if tpl[2] >= 0])/len([tpl[2] for tpl in self.data if tpl[2] >= 0])))
        # self.spendigsWidgets[0].setText(str(sum([tpl[2] for tpl in self.data if tpl[2] <= 0])/len([tpl[2] for tpl in self.data if tpl[2] >= 0])))
        # self.incomeWidgets[1].setText(str(max([tpl[2] for tpl in self.data if tpl[2] >= 0])))
        # self.spendigsWidgets[1].setText(str(min([tpl[2] for tpl in self.data if tpl[2] <= 0])))
        for comm in [["self.balanceWidget.setText(str(sum([tpl[2] for tpl in self.data])))", "self.balanceWidget.setText('0')"],
                     ["self.incomeWidgets[0].setText(str(sum([tpl[2] for tpl in self.data if tpl[2] >= 0])/len([tpl[2] for tpl in self.data if tpl[2] >= 0])))", "self.incomeWidgets[0].setText('0')"],
                     ["self.spendingsWidgets[0].setText(str(sum([tpl[2] for tpl in self.data if tpl[2] <= 0])/len([tpl[2] for tpl in self.data if tpl[2] >= 0])))", "self.spendingsWidgets[0].setText('0')"],
                     ["self.incomeWidgets[1].setText(str(max([tpl[2] for tpl in self.data if tpl[2] >= 0])))", "self.incomeWidgets[1].setText('0')"],
                     ["self.spendingsWidgets[1].setText(str(min([tpl[2] for tpl in self.data if tpl[2] <= 0])))", "self.spendingsWidgets[1].setText('0')"]
                     ]:
            try:
                exec(comm[0])
            except:
                exec(comm[1])
