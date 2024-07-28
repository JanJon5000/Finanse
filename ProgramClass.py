import sqlite3 as sql
from datetime import date
from PyQt5.QtWidgets import QLineEdit ,QPushButton ,QBoxLayout ,QApplication, QWidget, QLabel, QGridLayout, QMessageBox, QCalendarWidget, QComboBox, QListWidget, QListWidgetItem
from fundamentalClasses import SQL_SINGLE_INSTANCE, transaction, person, category
from customPYQT5Objects import QCustomFilterWidget, QAddBoxWidget

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
        self.populate_grid(self.g)
        
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
    
    def populate_grid(self, g: QGridLayout) -> None:
        # custom widget by which the user can add a transaction to his history
        self.adder = QAddBoxWidget()
        g.addWidget(self.adder, 0, 0)
        # QlineEdit with number of records to be shown
        self.recordBox = QLineEdit(self)
        self.recordBox.setMaxLength(2)
        self.recordBox.textChanged.connect(self.change_record_num)
        self.g.addWidget(self.recordBox, 1, 0)
        # Button creating a diagram out of wanted records
        self.g.addWidget(QLabel("wykres", self), 1, 1)
        # QCombo boxes which the user can use in order to filter the results
        # 1
        self.cursor.execute("SELECT personName FROM people WHERE 1=1")
        qListValues = self.cursor.fetchall()
        self.nameMultiComboBox = QCustomFilterWidget(self, qListValues, "Imie:")
        self.g.addWidget(self.nameMultiComboBox, 2, 0)
        # 2
        
        self.g.addWidget(QLabel("kategoria", self), 2, 1)
        self.g.addWidget(QLabel("kasa", self), 2, 2)
        self.g.addWidget(QLabel("data", self), 2, 3)


        
        # filtered data
        counter = 3
        self.show_table(self.filters, self.orderFilters, self.settings['rowNumber'])
        for record in self.shownContent:
            for i in range(len(record)):
                g.addWidget(QLabel(str(record[i]), self), counter, i)
            counter += 1

        self.setLayout(g)

    def refresh(self) -> None:
        self.clear_layout(self.g)
        self.populate_grid(self.g)
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