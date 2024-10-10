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
        self.spendigsWidgets = [QLabel("test0"), QLabel("test")]
        columnCounter = 0
        for l in [self.infoTexts, self.incomeWidgets, self.spendigsWidgets]:
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