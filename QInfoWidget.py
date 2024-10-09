from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout

class QInfoWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.accessibleLayout = QVBoxLayout()
        self.populateLayout()

    def populateLayout(self):
        self.balanceWidget = QLabel()
        self.balanceWidget.setObjectName("balance")
        
        self.spendigsWidget = QLabel()
        self.spendigsWidget.setObjectName("spendings")
        
        self.incomeWidget = QLabel()
        self.incomeWidget.setObjectName("income")

        self.periodOfTimeWidget = QLabel()
        self.periodOfTimeWidget.setObjectName("time")

        self.avarageSpending = QLabel()
        self.avarageIncome = QLabel()
        self.maxSpending = QLabel()
        self.minSPending = QLabel()
        self.maxIncome = QLabel()
        self.minIncome = QLabel()

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