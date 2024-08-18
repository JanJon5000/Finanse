import sqlite3 as sql
from datetime import date
from PyQt5.QtCore import QRect, QPropertyAnimation, QSize, QPoint, QDate
from PyQt5.QtWidgets import QLineEdit ,QPushButton ,QVBoxLayout, QWidget, QLabel, QGridLayout, QMessageBox, QCalendarWidget, QComboBox, QListWidget, QListWidgetItem, QHBoxLayout, QDateEdit
from fundamentalClasses import SQL_SINGLE_INSTANCE, transaction, person, category
from QAddBoxClass import QAddBoxWidget
from QFilteringWidgets import QFTLFilter, QListFilter, QFromToFilter
from pprint import pprint

class CORE(SQL_SINGLE_INSTANCE):
    def __init__(self):
        super().__init__()
        self.filters = dict()
        self.shownContent = list()
        
    def show_table(self, filters: dict, orderFilters: list,  limit: int) -> None:
        command = "SELECT people.personName, categories.name, transactions.money, transactions.date FROM transactions LEFT JOIN categories ON transactions.idCategory = categories.idCategory LEFT JOIN people ON transactions.idOfOther = people.idOfOther "
        self.filters = filters
        self.orderFilters = orderFilters

        if self.filters == dict():
            pass
        else:
            command += " WHERE "
            for key in list(self.filters.keys()):
                command += self.filters[key]
                if list(self.filters.keys()).index(key) != len(list(self.filters.keys()))-1:
                    command += " AND "

        if orderFilters == []:
            pass
        else:
            command += " ORDER BY "
            for element in self.orderFilters:
                command += f" {element[0]}"
                if element[1] == 1: command += ' ASC '
                else: command += " DESC "
        command += f" LIMIT {limit};"
        print(command)
        self.cursor.execute(command)
        self.shownContent = self.cursor.fetchall()
        print(self.shownContent)
    def show_graph() -> None: 
        pass


class Program(CORE, QWidget):
    def __init__(self, parent=None):
        #abstract which helps governing the program
        super().__init__()
        QWidget.__init__(self, parent)
        self.setWindowTitle('Finance Organizer')
        if self.cursor.execute("SELECT * FROM settings").fetchall() == []:
            self.cursor.execute("INSERT INTO settings VALUES (?, ?, ?)", [1000, 1000, 20])
            self.connection.commit()
        self.cursor.execute("SELECT * FROM settings")
        placeholder = list(self.cursor.fetchall()[0])
        self.settings = dict()
        self.settings["height"] = placeholder[0]
        self.settings["width"] = placeholder[1]
        self.settings["rowNumber"] = placeholder[2]
        self.orderFilters = []
        self.filterContents = dict()
        #setting the layout to grid
        self.mainGrid = QGridLayout()
        self.populate_grid()
        
        self.setGeometry(100, 100, self.settings["width"], self.settings["height"])
        self.show()

    #function cleaning the grid
    def clear_layout(self, layout):
        self.filterContents = dict()
        if layout is not None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget().objectName() == 'filterStatus':
                    self.clear_layout(child.widget().layout())
                if child.widget() is not None:
                    child.widget().deleteLater()
                    if isinstance(child.widget(), QFTLFilter):
                        lst = [child.widget().flag]
                        self.filterContents[child.widget().objectName()] = lst
                        dataWidg = child.widget().layout().itemAt(1).widget()
                        if isinstance(dataWidg, QListFilter):
                            lst.append([item.text() for item in dataWidg.qListPart.selectedItems()])
                        elif isinstance(dataWidg, QFromToFilter):
                            if isinstance(dataWidg.smallerData, QLineEdit):
                                lst.append([dataWidg.smallerData.text(), dataWidg.biggerData.text()])
                            elif isinstance(dataWidg.smallerData, QDateEdit):
                                lst.append([dataWidg.smallerData.date(), dataWidg.biggerData.date()])
                        self.filterContents[child.widget().objectName()] = lst
                    elif isinstance(child.widget(), QListFilter):
                        lst = [item.text() for item in child.widget().qListPart.selectedItems()]
                        self.filterContents[child.widget().objectName()] = lst
                elif child.layout() is not None:
                    self.clear_layout(child.layout())

    def populate_grid(self) -> None:
        ############        FILTERS AND SETTINGS - COLUMN 0
        # That column is its own widget since it has to have its own setting as a group
        # widget responsible for how the data is ordered
        self.consolidatedFilterWidget = QWidget()
        self.consolidatedFilterWidget.setMaximumWidth(300)
        self.consolidatedFilterWidget.setObjectName('filterStatus')
        self.filterLayout = QVBoxLayout()

        # print(self.filterContents)

        # widget responsible for determining which 'date range' is supposed to be shown
        self.cursor.execute("SELECT date from transactions WHERE 1=1")
        dates = [tpl[0] for tpl in self.cursor.fetchall()]
        dates = [date(int(i[0:4]), int(i[5:7]), int(i[8:])) for i in dates]
        dates = list(set(dates))
        dates.sort()
        if dates == []:
            dates.append(date.today())
        if 'transactions.date' not in list(self.filterContents.keys()):
            self.dataFilter = QFTLFilter(max(dates), min(dates), dates, 0)
        else:
            self.dataFilter = QFTLFilter(max(dates), min(dates), dates, self.filterContents['transactions.date'][0])
            self.dataFilter.currentFilter[self.filterContents['transactions.date'][0]].select_items(self.filterContents['transactions.date'][1])
        self.dataFilter.setObjectName('transactions.date')
        self.filterLayout.addWidget(self.dataFilter)

        # widget responsible for determining which 'ammount range' is supposed to be displayed
        self.cursor.execute("SELECT money FROM transactions WHERE 1=1")
        sums = [i[0] for i in self.cursor.fetchall()]
        sums = list(set(sums))
        sums.sort()
        if sums == []:
            sums.append(0.0)
        if 'transactions.money' not in list(self.filterContents.keys()):
            self.sumFilter = QFTLFilter(max(sums), min(sums), sums, 0)
        else:
            self.sumFilter = QFTLFilter(max(sums), min(sums), sums, self.filterContents['transactions.money'][0])
            self.sumFilter.currentFilter[self.filterContents['transactions.money'][0]].select_items(self.filterContents['transactions.money'][1])
        self.sumFilter.setObjectName('transactions.money')
        self.filterLayout.addWidget(self.sumFilter)

        # widget responsible for determining which categories are supposed to be displayed
        self.cursor.execute('SELECT name FROM categories WHERE 1=1')
        cats = [i[0] for i in list(set(self.cursor.fetchall()))]
        cats.sort()
        self.categoryFilter = QListFilter(cats)
        if 'categories.name' in list(self.filterContents.keys()):
            self.categoryFilter.select_items(self.filterContents['categories.name'])
        self.categoryFilter.setObjectName('categories.name')
        self.filterLayout.addWidget(self.categoryFilter)
        
        # widget responsible for determining which names are supposed to be displayed
        self.cursor.execute('SELECT personName FROM people WHERE 1=1')
        people = [i[0] for i in list(set(self.cursor.fetchall()))]
        self.peopleFilter = QListFilter(people)
        if 'people.PersonName' in list(self.filterContents.keys()):
            self.peopleFilter.select_items(self.filterContents['people.PersonName'])
        self.peopleFilter.setObjectName('people.PersonName')
        self.filterLayout.addWidget(self.peopleFilter)

        # QlineEdit setting the number of records to be displayed
        self.recordFilter = QLineEdit(self)
        self.recordFilter.setMaxLength(2)
        self.recordFilter.textChanged.connect(self.change_record_num)
        self.filterLayout.addWidget(self.recordFilter)

        # button applying filters
        self.applyLabel = QLabel('')
        self.applyButton = QPushButton("zastosuj")
        self.applyButton.clicked.connect(self.refresh)
        self.applywWidget = QWidget()
        self.applyLayout = QHBoxLayout()
        self.applyLayout.addWidget(self.applyLabel)
        self.applyLayout.addWidget(self.applyButton)
        self.applywWidget.setLayout(self.applyLayout)
        self.applywWidget.setObjectName('applyButton')
        self.filterLayout.addWidget(self.applywWidget)

        self.consolidatedFilterWidget.setLayout(self.filterLayout)
        with open("styleSHEETS/qfilter_stylesheet.qss", 'r') as file:
            style = file.read()
            self.consolidatedFilterWidget.setStyleSheet(style)
        self.mainGrid.addWidget(self.consolidatedFilterWidget, 0, 0, 7, 1)
        ############        OTHER - ROW 0
        # a button which opens up a dialog window with ability to add new data to db
        self.adderButton = QPushButton('dodaj transakcje', self)
        self.adderButton.clicked.connect(self.showAdderDialog)
        self.mainGrid.addWidget(self.adderButton, 0, 1)

        # PLACEHOLDER  a button tht generates and displays diagram out of displayed data
        self.diagramButton = QLabel('PLACEHOLDER')
        self.mainGrid.addWidget(self.diagramButton, 0, 2)

        # seperate widget with seperate layout of the data, after ordering after filters
        dataWidget = QWidget()
        dataLayout = QGridLayout()
        counter = 0
        self.show_table(self.filters, self.orderFilters, self.settings['rowNumber'])
        # printing all the categories in their colors
        self.cursor.execute('SELECT name, RGB FROM categories WHERE 1=1')
        colors = self.cursor.fetchall()
        colors = {tpl[0]:[int(i) for i in tpl[1].split(',')] for tpl in colors}
        # setting the colors of 'money' value depending on its 'isIncome' property
        for record in self.shownContent:
            for i in range(len(record)):
                if i != 4:
                    placeholder = QLabel(str(record[i]))
                else: continue
                if i == 1:
                    placeholder.setStyleSheet(f"color: rgb({colors[record[i]][0]}, {colors[record[i]][1]}, {colors[record[i]][2]});")
                if i == 2:
                    if record[-2] == abs(record[-2]):
                        placeholder.setStyleSheet("color: rgb(0, 255, 0);")
                    else:
                        placeholder = QLabel('-' + str(record[2]), self)
                        placeholder.setStyleSheet("color: rgb(255, 0, 0)")
                dataLayout.addWidget(placeholder, counter, i)
            counter += 1
        dataWidget.setLayout(dataLayout)
        self.mainGrid.addWidget(dataWidget, 1, 1, 4, 2)

        self.setLayout(self.mainGrid)

    def refresh(self) -> None:
        self.clear_layout(self.mainGrid)
        self.filters = dict()
        for key in list(self.filterContents.keys()):
            if len(self.filterContents[key]) != 0:
                if (isinstance(self.filterContents[key][0], bool) or isinstance(self.filterContents[key][0], int)) and self.filterContents[key][0] == 0:
                    if isinstance(self.filterContents[key][1][0], QDate):
                        self.filters[key] = f" {key} BETWEEN '{self.filterContents[key][1][0].toPyDate().strftime('%Y-%m-%d')}' AND '{self.filterContents[key][1][1].toPyDate().strftime('%Y-%m-%d')}' "
                    elif isinstance(self.filterContents[key][1][0], str):
                        try:
                            self.filters[key] = f" {key} BETWEEN {float(self.filterContents[key][1][0])} "
                        except:
                            self.filters[key] = f" {key} BETWEEN {float(self.sumFilter.currentFilter[self.sumFilter.flag].minValue)} "
                        try:
                            self.filters[key] += f" AND {float(self.filterContents[key][1][1])} "
                        except:
                            self.filters[key] += f" AND {float(self.sumFilter.currentFilter[self.sumFilter.flag].maxValue)} "
                elif (isinstance(self.filterContents[key][0], bool) or isinstance(self.filterContents[key][0], int)) and self.filterContents[key][0] == 1 and len(self.filterContents[key][1]) != 0:
                    if isinstance(self.filterContents[key][1][0], QDate):
                        self.filters[key] = ''
                        for val in self.filterContents[key][1]:
                            self.filters[key] += f" {key} = '{val.toPyDate().strftime('%Y-%m-%d')}' "
                            if self.filterContents[key][1].index(val) != len(self.filterContents[key][1])-1:
                                self.filters[key] += " OR "
                    elif isinstance(self.filterContents[key][1][0], str):
                        self.filters[key] = ''
                        for val in self.filterContents[key][1]:
                            self.filters[key] += f" {key} = {float(val)} "
                            if self.filterContents[key][1].index(val) != len(self.filterContents[key][1])-1:
                                self.filters[key] += " OR "
                else:
                    self.filters[key] = ''
                    for val in self.filterContents[key]:
                        self.filters[key] += f" {key} = '{val}' "
                        if self.filterContents[key].index(val) != len(self.filterContents[key])-1:
                            self.filters[key] += " OR "
        self.populate_grid()
        self.update()

    def change_record_num(self, text) -> None:
        text = self.recordFilter.text()
        try:
            text = int(text)
            self.settings['rowNumber'] = text
            self.cursor.execute("DELETE FROM settings WHERE 1=1")
            self.cursor.execute("INSERT INTO settings VALUES (?, ?, ?)", (self.settings['height'], self.settings['width'], text))
            self.connection.commit()
        except:
            pass

    def closeEvent(self, event):
        new_size = self.size()
        try:
            self.cursor.execute("DELETE FROM settings WHERE 1=1")
            self.cursor.execute("INSERT INTO settings VALUES (?, ?, ?)", (new_size.height(), new_size.width(), self.settings['rowNumber']))
            self.connection.commit()
        except sql.Error as e:
            print(f"error {e}")
        finally:
            self.cursor.close()
            self.connection.close()
        super().closeEvent(event)
    
    def showAdderDialog(self):
        self.dialog = QAddBoxWidget(self)
        button_geometry = self.adderButton.geometry()
        global_button_pos = self.adderButton.mapToGlobal(QPoint(0, self.adderButton.height()))
        self.dialog.setMinimumSize(1, 1)
        self.dialog.setGeometry(QRect(global_button_pos.x(), global_button_pos.y() + button_geometry.y(), 1, 1))
        self.dialog.closed.connect(self.refresh)

        self.animation = QPropertyAnimation(self.dialog, b"size")
        self.animation.setDuration(300)
        self.animation.setStartValue(QSize(1, 1))
        self.animation.setEndValue(QSize(1000, 300))
        self.animation.start()
        self.dialog.exec_()