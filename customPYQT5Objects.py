from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QLineEdit ,QPushButton, QWidget, QGridLayout, QScrollArea, QListWidget, QLabel, QCalendarWidget, QCheckBox
from fundamentalClasses import SQL_SINGLE_INSTANCE
import traceback

class QCustomFilterWidget(QWidget):
    def __init__(self, parent = None, qListValues = [], name = "") -> None:
        super().__init__()
        QWidget.__init__(self, parent)

        self.qLabelPart = QLabel(name, self)
        self.qScrollPart = QScrollArea(self)

        # customizing scrollable part - a list
        self.qScrollPart.setWidgetResizable(True) 
        self.qListPart = QListWidget(self)
        self.qListPart.addItems(qListValues)
        self.qListPart.setSelectionMode(QListWidget.ExtendedSelection)
        self.qScrollPart.setWidget(self.qListPart)
        self.qScrollPart.setFixedSize(300, 300)

        # a fixed layout of the widget
        self.accesibleLayout = QGridLayout(self)
        self.accesibleLayout.addWidget(self.qLabelPart, 0, 0)
        self.accesibleLayout.addWidget(self.qScrollPart, 1, 0)

        self.setLayout(self.accesibleLayout)

class QAddBoxWidget(QWidget, SQL_SINGLE_INSTANCE):
    def __init__(self, parent=None) -> None:
        super().__init__()
        QWidget.__init__(self, parent)
        SQL_SINGLE_INSTANCE.__init__(self)
        
        self.accessibleLayout = QGridLayout(self)
        self.qButtonPart = QPushButton("dodaj", self)

        self.qLabels = [QLabel(text, self) for text in ('imie', 'kategoria', 'kwota', 'przychód', 'data')]
        self.qInteractiveComps = [QLineEdit(self), QLineEdit(self), QLineEdit(self), QCheckBox(self), QCalendarWidget(self)]

        # setup of the interactive elements in the widget:

        # name QlineEdit
        

        # setup of the layout        
        for i in [0, 1, 2, 3]:
            self.accessibleLayout.addWidget(self.qLabels[i], i, 0)
        for i in [0, 1, 2, 3]:
            self.accessibleLayout.addWidget(self.qInteractiveComps[i], i, 1)
        self.accessibleLayout.addWidget(self.qLabels[4], 0, 2)
        self.accessibleLayout.addWidget(self.qInteractiveComps[4], 1, 2, 1, 4)

        self.accessibleLayout.addWidget(self.qButtonPart, 4, 0, 1, 5)
        self.setLayout(self.accessibleLayout)