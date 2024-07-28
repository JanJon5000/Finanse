from PyQt5.QtCore import Qt, QStringListModel, QLocale
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QLineEdit ,QPushButton, QWidget, QGridLayout, QScrollArea, QListWidget, QLabel, QCalendarWidget, QCheckBox, QCompleter
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
        
        self.populateGrid()
    
    def populateGrid(self):
        # Constructors of the objects
        self.accessibleLayout = QGridLayout(self)
        self.qButtonPart = QPushButton("dodaj", self)
        self.qLabels = [QLabel(text, self) for text in ('imie', 'kategoria', 'kwota', 'przychód', 'data')]
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
        self.qButtonPart.clicked.connect(self.add_transaction)
        ########### QCALLENDAR
        self.qInteractiveComps[-1].setGridVisible(True)
        self.qInteractiveComps[-1].setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.qInteractiveComps[-1].setLocale(QLocale(QLocale.Polish))
        # setup of the layout        
        for i in range(4):
            self.accessibleLayout.addWidget(self.qLabels[i], i, 0)  
            self.accessibleLayout.addWidget(self.qInteractiveComps[i], i, 1)
        self.accessibleLayout.addWidget(self.qLabels[4], 0, 2)
        self.accessibleLayout.addWidget(self.qInteractiveComps[4], 1, 2, 1, 4)

        self.accessibleLayout.addWidget(self.qButtonPart, 4, 0, 1, 5)
        self.setLayout(self.accessibleLayout)

    def add_transaction(self): 
        print('test')

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