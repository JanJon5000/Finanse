from PyQt5.QtCore import QStringListModel, QLocale, pyqtSignal
from PyQt5.QtWidgets import QLineEdit ,QPushButton, QWidget, QGridLayout, QLabel, QCalendarWidget, QCompleter, QDialog
from fundamentalClasses import SQL_SINGLE_INSTANCE, person, transaction, category
from datetime import date
from random import randint

class QAddBoxWidget(QDialog, SQL_SINGLE_INSTANCE):
    # signal that is emited when dialog window is close
    # so that the program class can act on it and create transactions/categories/recipients
    closed = pyqtSignal()
    def __init__(self, parent=None) -> None:
        super().__init__()
        QDialog.__init__(self, parent)
        SQL_SINGLE_INSTANCE.__init__(self)
        self.populateGrid()
    
    def populateGrid(self):
        self.accessibleLayout = QGridLayout(self)
        self.innerLayout = QGridLayout()
        self.qButtonPart = QPushButton("dodaj", self)
        self.qLabels = [QLabel(text, self) for text in ('imie', 'kategoria', 'kwota')]
        self.qInteractiveComps = [QLineEdit(self), QLineEdit(self), QLineEdit(self), QCalendarWidget(self)]

        ########### QLINEEDITS
        # suggestions(completers) - list of suggested words for every interactive text field in the widget
        # in case the user wants to add a transaction with already existing category/recipient/sender
        # of said money
        self.setCompleters()

        self.qButtonPart.clicked.connect(self.on_click_button)
        # parameters of callendar - language, headers  and grid
        self.qInteractiveComps[-1].setGridVisible(True)
        self.qInteractiveComps[-1].setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.qInteractiveComps[-1].setLocale(QLocale(QLocale.Polish))

        with open('styleSHEETS/callendar-stylesheet.qss', 'r') as file:
            self.qInteractiveComps[-1].setStyleSheet(file.read())
        # setup inner of the layout (with interactive elements - text fields and their labels)
        for i in range(3):
            self.innerLayout.addWidget(self.qLabels[i], i, 0)  
            self.innerLayout.addWidget(self.qInteractiveComps[i], i, 1)
        self.innerLayout.setContentsMargins(5, 5, 5, 5)
        self.innerLayout.setHorizontalSpacing(5)
        self.innerLayout.setVerticalSpacing(5)
        # inner widget with those interactive elements
        self.innerWidget = QWidget()
        self.innerWidget.setLayout(self.innerLayout)
        # setup of the outer layout - callendar + smaller widget + button
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
        # checking if the data was properly written
        if data[0] != '' and data[1] != '' and data[2] != '':
            data[2] = data[2].replace(',', '.')
            code_lines = [
                "if float(data[2]) != 0.0: selectedData['money'] = float(data[2])",
                "selectedData['isIncome'] = data[3]",
                "selectedData['date'] = date(data[-1].year(), data[-1].month(), data[-1].day())"
            ]
            selectedData = dict()
            for line in code_lines:
                try:
                    exec(line)
                except:
                    pass
            # trying to find the ids of category and the other person in the transaction
            # if non existant, program adds them
            forList = [
                (f"SELECT idOfOther FROM people WHERE personName = '{data[0]}'", 
                 "self.create_new_person(person(None, data[0]))", 
                 'idOfOther'),
                (f"SELECT idCategory FROM categories WHERE name = '{data[1]}'", 
                 "self.create_new_category(category(None, data[1], str(randint(0,255)) + ',' + str(randint(0,255)) + ',' + str(randint(0,255))))",
                 'idCategory')
            ]
            for (command, objectExec, sqlIndex) in forList:
                self.cursor.execute(command)
                placeholder = self.cursor.fetchall()
                if len(placeholder) < 1:
                    exec(objectExec)
                self.cursor.execute(command)
                selectedData[sqlIndex] = self.cursor.fetchall()[0][0]
            self.create_new_transaction(transaction(selectedData['date'], selectedData['money'], selectedData['idCategory'], selectedData['idOfOther']))
            self.refresh()

    def setCompleters(self) -> None:
        self.suggestions = []
        for (value, table) in [('personName', 'people'), ('name', 'categories')]:
            self.cursor.execute(f"SELECT {value} FROM {table} WHERE 1=1")
            data = self.cursor.fetchall()
            
            self.suggestions.append([''.join(tpl) for tpl in data])
        # models with ques on what categories/people there are in the database
        self.models = [QStringListModel(self.suggestions[i], self) for i in range(len(self.suggestions))]
        # compeleters - objects giving hints in the qlineedit boxes (corresponding to interactive text fields)
        self.completers = [QCompleter(self.models[i], self) for i in range(len(self.models))]
        for i in range(len(self.completers)): 
            self.completers[i].setCaseSensitivity(False)
            self.qInteractiveComps[i].setCompleter(self.completers[i])
            self.qInteractiveComps[i].clear()
        self.qInteractiveComps[-2].clear()
        
    def refresh(self):
        self.setCompleters()
        self.update()
    
    def closeEvent(self, event) -> None:
        self.closed.emit()
        super().closeEvent(event)