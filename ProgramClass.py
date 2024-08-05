import sqlite3 as sql
from datetime import date
from PyQt5.QtCore import QRect, QPropertyAnimation, QSize
from PyQt5.QtWidgets import QLineEdit ,QPushButton ,QBoxLayout ,QApplication, QWidget, QLabel, QGridLayout, QMessageBox, QCalendarWidget, QComboBox, QListWidget, QListWidgetItem
from fundamentalClasses import SQL_SINGLE_INSTANCE, transaction, person, category
from customPYQT5Objects import QFilterWidget, QAddBoxWidget

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
        self.g = QGridLayout()
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
        # custom widget by which the user can add a transaction to his history
        self.adderButton = QPushButton('dodaj tranzakcje', self)
        self.adderButton.clicked.connect(self.showAdderDialog)
        self.g.addWidget(self.adderButton, 0, 0)

        # QlineEdit with number of records to be shown
        self.recordBox = QLineEdit(self)
        self.recordBox.setMaxLength(2)
        self.recordBox.textChanged.connect(self.change_record_num)
        self.g.addWidget(self.recordBox, 1, 0)
        # Button creating a diagram out of visible transactions
        self.g.addWidget(QLabel("wykres", self), 1, 1)
        # QComboboxes which the user can use in order to filter the results
        # 1
        self.cursor.execute("SELECT personName FROM people WHERE 1=1")
        qListValues = self.cursor.fetchall()
        qListValues = [''.join(tpl) for tpl in qListValues]
        self.nameMultiComboBox = QFilterWidget(self, qListValues, "Imie:")
        self.g.addWidget(self.nameMultiComboBox, 2, 0)
        # 2
        self.cursor.execute("SELECT name FROM categories WHERE 1=1")
        qListValues = self.cursor.fetchall()
        qListValues = [''.join(tpl) for tpl in qListValues]
        self.categoryMultiComboBox = QFilterWidget(self, qListValues, "Kategoria:")
        self.g.addWidget(self.categoryMultiComboBox, 2, 1)
        # SOON a widget with a scroll bar to choose money range
        self.g.addWidget(QLabel("kasa", self), 2, 2)
        # SOON a callendar/scroll bar to choose date range
        self.g.addWidget(QLabel("data", self), 2, 3)
        
        # filtered data
        counter = 3
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
                self.g.addWidget(placeholder, counter, i)
            counter += 1

        self.setLayout(self.g)

    def refresh(self) -> None:
        self.clear_layout(self.g)
        self.populate_grid()
        self.update()

    def change_record_num(self, text) -> None:
        text = self.recordBox.text()
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
        global_button_pos = self.adderButton.mapToGlobal(button_geometry.topLeft())
        self.dialog.setMinimumSize(1, 1)
        self.dialog.setGeometry(QRect(global_button_pos.x(), global_button_pos.y() + button_geometry.height(), 1, 1))
        self.dialog.closed.connect(self.refresh)

        self.animation = QPropertyAnimation(self.dialog, b"size")
        self.animation.setDuration(300)
        self.animation.setStartValue(QSize(1, 1))
        self.animation.setEndValue(QSize(1000, 300))
        self.animation.start()
        self.dialog.exec_()

        