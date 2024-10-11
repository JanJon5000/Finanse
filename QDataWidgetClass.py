from fundamentalClasses import SQL_SINGLE_INSTANCE, person, transaction, category
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QLineEdit, QDateEdit
from PyQt5.QtCore import QDate, pyqtSignal
from PyQt5.QtGui import QDoubleValidator
from random import randint

class QDataWidget(QWidget):
    dataChanged = pyqtSignal()
    def __init__(self, variables: list, colors: list) -> None:
        super().__init__()
        self.readLayout = QHBoxLayout()
        self.currentIndex = 0
        self.variables = variables
        self.prevVariables = variables
        self.colors = colors

        self.populateLine()
        self.setLayout(self.readLayout)

    def populateLine(self):
        if self.currentIndex == 0:
            for x in self.variables:
                x = QLabel(str(x))
                try: 
                    if self.variables.index(x.text()) == 1:
                        x.setStyleSheet(f"color: rgb({self.colors[0]}, {self.colors[1]}, {self.colors[2]});")
                    if self.variables.index(x.text()) == 2:
                        x.setText(x.text().replace(',', '.'))
                        if float(x.text()) == abs(float(x.text())):
                            x.setStyleSheet("color: rgb(0, 255, 0);")
                        else:
                            x = QLabel('-' + x.text())
                            x.setStyleSheet("color: rgb(255, 0, 0);")
                except:
                    if self.variables.index(float(x.text())) == 1:
                        x.setStyleSheet(f"color: rgb({self.colors[0]}, {self.colors[1]}, {self.colors[2]});")
                    if self.variables.index(float(x.text())) == 2:
                        if float(x.text()) == abs(float(x.text())):
                            x.setStyleSheet("color: rgb(0, 255, 0);")
                        else:
                            x.setStyleSheet("color: rgb(255, 0, 0);")
                self.readLayout.addWidget(x)
            x = QPushButton("Edycja")
            x.clicked.connect(self.changeLayout)
            self.readLayout.addWidget(x)
        elif self.currentIndex == 1:
            for x in self.variables:
                x = QLineEdit(str(x))
                try:
                    if self.variables.index(x.text()) == 2:
                        if float(x.text()) == abs(float(x.text())):
                            pass
                        else:
                            x = QLineEdit('-' + x.text())
                except:
                    if self.variables.index(float(x.text())) == 2:
                        x.setText(x.text().replace('.', ','))
                        double_validator = QDoubleValidator(float('-inf'), float('inf'), 2)
                        double_validator.setNotation(QDoubleValidator.StandardNotation)
                        x.setValidator(double_validator)
                try:
                    if self.variables.index(x.text()) == 3:
                        x = QDateEdit(QDate(int(x.text()[:4]), int(x.text()[5:7]), int(x.text()[8:])))
                        x.setDisplayFormat("yyyy-MM-dd")
                except ValueError: pass
                self.readLayout.addWidget(x)
            x = QPushButton("Zapisz zmiany")
            x.clicked.connect(self.changeLayout)
            x.clicked.connect(self.dataChanged.emit)
            self.readLayout.addWidget(x)

    def changeLayout(self):
        self.clear_layout(self.layout())
        self.currentIndex = not self.currentIndex
        self.updateValues()
        self.populateLine()
        self.update()

    def updateValues(self):
        deleteRecordData = []
        newRecordData = []
        HANDLE = SQL_SINGLE_INSTANCE()
        for index in range(len(self.prevVariables)):
            if self.prevVariables[index] == '':
                self.prevVariables[index] = self.variables[index]
            if index == 2 and isinstance(self.prevVariables[index], str):
                self.prevVariables[index] = float(self.prevVariables[index].replace(',', '.'))
            if self.prevVariables[index] != self.variables[index]:
                if index == 0:
                    HANDLE.cursor.execute(f"SELECT * FROM people WHERE personName = '{self.prevVariables[index]}'")
                    Data = HANDLE.cursor.fetchall()
                    if len(Data) == 0:
                        HANDLE.create_new_person(person(0, self.prevVariables[index]))
                if index == 1:
                    HANDLE.cursor.execute(f"SELECT * FROM categories WHERE name = '{self.prevVariables[index]}'")
                    Data = HANDLE.cursor.fetchall()
                    if len(Data) == 0:
                        HANDLE.create_new_category(category(0, self.prevVariables[index], f"{randint(0, 255)},{randint(0, 255)},{randint(0, 255)}"))           
        HANDLE.cursor.execute(f"SELECT idOfOther FROM people WHERE personName = '{self.prevVariables[0]}'")
        newRecordData.append(HANDLE.cursor.fetchall()[0][0])
        HANDLE.cursor.execute(f"SELECT idCategory FROM categories WHERE name = '{self.prevVariables[1]}'")
        newRecordData.append(HANDLE.cursor.fetchall()[0][0])

        HANDLE.cursor.execute(f"SELECT idOfOther FROM people WHERE personName = '{self.variables[0]}'")
        deleteRecordData.append(HANDLE.cursor.fetchall()[0][0])
        HANDLE.cursor.execute(f"SELECT idCategory FROM categories WHERE name = '{self.variables[1]}'")
        deleteRecordData.append(HANDLE.cursor.fetchall()[0][0])
        
        HANDLE.cursor.execute(f"DELETE FROM transactions WHERE idCategory = '{deleteRecordData[1]}' AND idOfOther = '{deleteRecordData[0]}' AND date = '{self.variables[-1]}' AND money = {self.variables[2]}")
        HANDLE.create_new_transaction(transaction(self.prevVariables[-1], self.prevVariables[2], newRecordData[1], newRecordData[0]))
        self.variables = self.prevVariables

    def clear_layout(self, layout):
        self.prevVariables = []
        if layout is not None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget() is not None:
                    if not isinstance(child.widget(), QPushButton):
                        try:
                            self.prevVariables.append(child.widget().text())
                        except:
                            self.prevVariables.append(child.widget().date())
                    child.widget().deleteLater()
                elif child.layout() is not None:
                    self.clear_layout(child.layout())