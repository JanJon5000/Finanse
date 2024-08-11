import sqlite3 as sql
from datetime import date
from PyQt5.QtCore import QRect, QPropertyAnimation, QSize, QPoint
from PyQt5.QtWidgets import QLineEdit ,QPushButton ,QVBoxLayout ,QApplication, QWidget, QLabel, QGridLayout, QMessageBox, QCalendarWidget, QComboBox, QListWidget, QListWidgetItem
from fundamentalClasses import SQL_SINGLE_INSTANCE, transaction, person, category
from QAddBoxClass import QAddBoxWidget
from QFilteringWidgets import QFTLFilter, QOrderWidget

class CORE(SQL_SINGLE_INSTANCE):
    def __init__(self):
        super().__init__()
        self.filters = dict()
        self.shownContent = list()
        
    def show_table(self, filters: dict, orderFilters: list,  limit: int) -> None:
        command = "SELECT people.personName, categories.name, transactions.money, transactions.date, transactions.isIncome FROM transactions LEFT JOIN categories ON transactions.idCategory = categories.idCategory LEFT JOIN people ON transactions.idOfOther = people.idOfOther "
        self.filters = filters
        self.orderFilters = orderFilters
        if self.filters == dict():
            pass
        else:
            command += " WHERE "
            for key in self.filters.keys():
                for i in range(len(self.filters[key])):
                    command  += f" {key} = {self.filters[key][i]} "
                    if i != len(self.filters[key])-1:
                        command += " OR "
                if key != len(list(self.filters.keys()))-1:
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
        #setting the layout to grid
        self.mainGrid = QGridLayout()
        self.populate_grid()
        
        self.setGeometry(100, 100, self.settings["width"], self.settings["height"])
        self.show()

    #function cleaning the grid
    def clear_layout(self, layout):
        if layout is not None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget() is not None:
                    child.widget().deleteLater()
                elif child.layout() is not None:
                    self.clear_layout(child.layout())

    def populate_grid(self) -> None:
        ############        FILTERS AND SETTINGS - COLUMN 0
        # 'watermark' of my app
        self.logo = QLabel('logo')
        self.mainGrid.addWidget(self.logo, 0, 0)

        # widget responsible for how the data is ordered
        self.orderWidget = QOrderWidget(['data', 'kategoria', 'imie', 'kwota'])
        self.mainGrid.addWidget(self.orderWidget, 1, 0)

        # widget responsible for determining which 'date range' is supposed to be shown
        self.cursor.execute("SELECT date from transactions WHERE 1=1")
        dates = [tpl[0] for tpl in self.cursor.fetchall()]
        dates = [date(int(i[0:4]), int(i[5:7]), int(i[8:])) for i in dates]
        dates = list(set(dates))
        dates.sort()
        self.dataFilter = QFTLFilter(max(dates), min(dates), dates)
        self.mainGrid.addWidget(self.dataFilter, 2, 0)

        # PLACEHOLDER widget responsible for determining which 'ammount range' is supposed to be displayed
        self.cursor.execute("SELECT money FROM transactions WHERE 1=1")
        sums = [int(i[0]) for i in self.cursor.fetchall()]
        sums = list(set(sums))
        sums.sort()
        self.sumFilter = QFTLFilter(max(sums), min(sums), sums)
        self.mainGrid.addWidget(self.sumFilter, 3, 0)

        # PLACEHOLDER widget responsible for determining which categories are supposed to be displayed
        self.categoryFilter = QLabel('PLACEHOLDER')
        self.mainGrid.addWidget(self.categoryFilter, 4, 0)

        # QlineEdit setting the number of records to be displayed
        self.recordFilter = QLineEdit(self)
        self.recordFilter.setMaxLength(2)
        self.recordFilter.textChanged.connect(self.change_record_num)
        self.mainGrid.addWidget(self.recordFilter, 5, 0)

        # PLACEHOLDER buttons for deleting, applying filters and removing filters
        self.settingButtons = [QPushButton(text) for text in ('usuń', 'zastosuj', 'przywróc')]
        buttonLayout = QVBoxLayout()
        for b in self.settingButtons:
            buttonLayout.addWidget(b)
        buttonWidget = QWidget()
        buttonWidget.setLayout(buttonLayout)
        self.mainGrid.addWidget(buttonWidget, 6, 0)

        ############        OTHER - ROW 0
        # a button which opens up a dialog window with ability to add new data to db
        self.adderButton = QPushButton('dodaj tranzakcje', self)
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
                    if record[-1]:
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