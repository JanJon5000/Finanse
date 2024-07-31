from PyQt5.QtCore import Qt, QStringListModel, QLocale, pyqtSignal
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QLineEdit ,QPushButton, QWidget, QGridLayout, QScrollArea, QListWidget, QLabel, QCalendarWidget, QCheckBox, QCompleter, QDialog
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

class QAddBoxWidget(QDialog, SQL_SINGLE_INSTANCE):
    def __init__(self, parent=None) -> None:
        super().__init__()
        QDialog.__init__(self, parent)
        SQL_SINGLE_INSTANCE.__init__(self)
        self.closed = pyqtSignal()
        self.populateGrid()
    
    def populateGrid(self):
        # Constructors of the objects
        self.accessibleLayout = QGridLayout(self)
        self.innerLayout = QGridLayout(self)
        self.qButtonPart = QPushButton("dodaj", self)
        self.qLabels = [QLabel(text, self) for text in ('imie', 'kategoria', 'kwota', 'przychód')]
        self.qInteractiveComps = [QLineEdit(self), QLineEdit(self), QLineEdit(self), QCheckBox(self), QCalendarWidget(self)]

        # setup of the interactive elements in the widget:

        ########### QLINEEDITS
        # making a list of completers for every QlineEdit box
        # suggestion list:
        self.suggestions = []
        for (value, table) in [('personName', 'people'), ('name', 'categories')]:
            self.cursor.execute(f"SELECT {value} FROM {table} WHERE 1=1")
            data = self.cursor.fetchall()
            self.suggestions.append(data)
        # models with ques on what categories/people there are in the database
        self.models = [QStringListModel(self.suggestions[i], self) for i in range(len(self.suggestions))]
        # compeleters - objects giving hints in the qlineedit boxes
        self.completers = [QCompleter(self.models[i], self) for i in range(len(self.models))]
        for i in range(len(self.completers)): 
            self.completers[i].setCaseSensitivity(False)
            self.qInteractiveComps[i].setCompleter(self.completers[i])

        ########### QBUTTON
        self.qButtonPart.clicked.connect(self.on_click_button)
        ########### QCALLENDAR
        self.qInteractiveComps[-1].setGridVisible(True)
        self.qInteractiveComps[-1].setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.qInteractiveComps[-1].setLocale(QLocale(QLocale.Polish))
        with open('/Users/jan/VSCODE/Finanse/callendar-stylesheet.css', 'r') as file:
            self.qInteractiveComps[-1].setStyleSheet(file.read())
        # setup inner of the layout
        for i in range(4):
            self.innerLayout.addWidget(self.qLabels[i], i, 0)  
            self.innerLayout.addWidget(self.qInteractiveComps[i], i, 1)
        self.innerLayout.setContentsMargins(5, 5, 5, 5)
        self.innerLayout.setHorizontalSpacing(5)
        self.innerLayout.setVerticalSpacing(5)
        # inner widget with smaller elements
        self.innerWidget = QWidget()
        self.innerWidget.setLayout(self.innerLayout)
        # setup of the outer layout
        self.accessibleLayout.addWidget(self.innerWidget, 0, 0)
        self.accessibleLayout.addWidget(self.qInteractiveComps[-1], 0, 1)
        self.accessibleLayout.addWidget(self.qButtonPart, 1, 0, 1, 2)
        
        self.setLayout(self.accessibleLayout)

    def on_click_button(self):
        data = []
        for i in range(len(self.qInteractiveComps)):
            match self.qInteractiveComps[i]:
                case QLineEdit():
                    data.append(self.qInteractiveComps[i].text())
                case QCalendarWidget():
                    data.append(self.qInteractiveComps[i].selectedDate())
                case QCheckBox():
                    data.append(self.qInteractiveComps[i].isChecked())
        if(data[0] != '' and data[1] != '' and data[2] != ''):
            selectData = {"money":float(data[2]), 'isIncome':bool(data[3])}
            print(selectData)

    def clear_layout(self, layout):
        if layout is not None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget() is not None:
                    child.widget().deleteLater()
                elif child.layout() is not None:
                    self.clear_layout(child.layout())
    
    def refresh(self):
        self.clear_layout(self.accessibleLayout)
        self.populateGrid()
        self.update()