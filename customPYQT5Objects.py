from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QLineEdit ,QPushButton, QWidget, QGridLayout, QScrollArea, QListWidget, QLabel
from fundamentalClasses import SQL_SINGLE_INSTANCE
import traceback

class QCustomWidget(QWidget):
    def __init__(self, parent = None, qListValues = [], name = "") -> None:
        super().__init__()
        QWidget.__init__(self, parent)

        self.qLabelPart = QLabel(name, self)
        self.qScrollPart = QScrollArea(self)
        self.qLineEditPart = QLineEdit(self)
        self.qButtonPart = QPushButton(self)

        # customizing scrollable part - a list
        self.qScrollPart.setWidgetResizable(True)
        self.qListPart = QListWidget(self)
        self.qListPart.addItems(["test" for _ in range(100)])
        self.qListPart.setSelectionMode(QListWidget.MultiSelection)
        self.qScrollPart.setWidget(self.qListPart)
        self.qScrollPart.setFixedSize(300, 300)


        # a fixed layout of the widget
        self.accesibleLayout = QGridLayout(self)
        self.accesibleLayout.addWidget(self.qLabelPart, 0, 0, 1, 2)
        self.accesibleLayout.addWidget(self.qLineEditPart, 1, 0)
        self.accesibleLayout.addWidget(self.qButtonPart, 1, 1)
        self.accesibleLayout.addWidget(self.qScrollPart, 2, 0, 1, 2)

        self.setLayout(self.accesibleLayout)