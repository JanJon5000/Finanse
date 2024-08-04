from PyQt5.QtCore import Qt, QStringListModel, QLocale, pyqtSignal, QDate, QRect
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QLineEdit ,QPushButton, QWidget, QGridLayout, QScrollArea, QListWidget, QLabel, QCalendarWidget, QCheckBox, QCompleter, QDialog, QSlider
from fundamentalClasses import SQL_SINGLE_INSTANCE, person, transaction, category
import traceback
from datetime import date
from random import randint

class QCircle(QWidget):
    def __init__(self, widht: int, height: int, R:int, G:int, B:int, parent: QWidget | None) -> None:
        super().__init__()
        QWidget.__init__(self, parent)
        self.setGeometry(100, 100, widht, height)
        self.color = QColor(R, G, B)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QColor(self.RGB['R'], self.RGB['G'], self.RGB['B']))
        painter.setPen(QColor(0, 0, 0))

        rect = QRect(50, 50, 200, 200)
        painter.drawEllipse(rect)
    
    def setColor(self, color):
        self.color = color
        self.update()


class QColorPicker(QWidget):
    def __init__(self, parent: QWidget | None) -> None:
        super().__init__()
        QWidget.__init__(self, parent)

        # creating sliders and labels - all of the functional widget in the layout
        self.sliderList = [QSlider(Qt.Horizontal, self) for _ in range(3)]
        self.labelList = [QLabel(text, self) for text in ("red", 'blue', 'green')]
        # a circle representing a color which can be created using the RGB values
        self.CircleWidget = QCircle(200, 200, 0, 0, 0)
        

class QFilterWidget(QWidget):
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
    closed = pyqtSignal()
    def __init__(self, parent=None) -> None:
        super().__init__()
        QDialog.__init__(self, parent)
        SQL_SINGLE_INSTANCE.__init__(self)
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
        self.setCompleters()

        ########### QBUTTON
        self.qButtonPart.clicked.connect(self.on_click_button)
        ########### QCALLENDAR
        self.qInteractiveComps[-1].setGridVisible(True)
        self.qInteractiveComps[-1].setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.qInteractiveComps[-1].setLocale(QLocale(QLocale.Polish))
        with open('callendar-stylesheet.qss', 'r') as file:
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
            self.create_new_transaction(transaction(selectedData['date'], selectedData['money'], selectedData['idCategory'], selectedData['money'], selectedData['idOfOther']))
            self.refresh()

    def setCompleters(self) -> None:
        self.suggestions = []
        for (value, table) in [('personName', 'people'), ('name', 'categories')]:
            self.cursor.execute(f"SELECT {value} FROM {table} WHERE 1=1")
            data = self.cursor.fetchall()
            self.suggestions.append([''.join(tpl) for tpl in data])
        # models with ques on what categories/people there are in the database
        self.models = [QStringListModel(self.suggestions[i], self) for i in range(len(self.suggestions))]
        # compeleters - objects giving hints in the qlineedit boxes
        self.completers = [QCompleter(self.models[i], self) for i in range(len(self.models))]
        for i in range(len(self.completers)): 
            self.completers[i].setCaseSensitivity(False)
            self.qInteractiveComps[i].setCompleter(self.completers[i])
            self.qInteractiveComps[i].clear()
        self.qInteractiveComps[-3].clear()
        self.qInteractiveComps[-2].setChecked(False)


    def refresh(self):
        self.setCompleters()
        self.update()
    
    def closeEvent(self, event) -> None:
        self.closed.emit()
        super().closeEvent(event)