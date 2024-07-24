from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QLineEdit ,QPushButton, QWidget, QGridLayout, QComboBox, QCheckBox, QStyledItemDelegate
from fundamentalClasses import SQL_SINGLE_INSTANCE
import traceback

class QMultiComboBox(QComboBox):
    def __init__(self, parent=None, qListValues=None) -> None:
        super().__init__()
        QComboBox.__init__(self, parent)
        self.addItems(qListValues)
        self.chosenFilters = list()
        self.visiblePopup = False

    def showPopup(self):
        self.visiblePopup = True
        super().showPopup()

    def hidePopup(self) -> None:
        self.visiblePopup = False
        super().hidePopup()

    def mousePressEvent(self, event: QMouseEvent | None) -> None:
        i = 1
        print(event.button(), Qt.RightButton)
        if int(event.button()) == int(Qt.RightButton):
            print('dziala!')
        if int(event.button()) == int(Qt.LeftButton) and self.visiblePopup == False:
            super().mousePressEvent(event)

class QCustomWidget(QWidget):
    def __init__(self, parent = None) -> None:
        super().__init__()
        QWidget.__init__(self, parent)

        self.qListPart = QMultiComboBox(self, qListValues=['asd', 'aaa', 'sss'])
        self.qLineEditPart = QLineEdit(self)
        self.qButtonPart = QPushButton(self)

        self.accesibleLayout = QGridLayout(self)
        self.accesibleLayout.addWidget(self.qLineEditPart, 0, 0)
        self.accesibleLayout.addWidget(self.qButtonPart, 0, 1)
        self.accesibleLayout.addWidget(self.qListPart, 1, 0, 1, 2)

        self.setLayout(self.accesibleLayout)