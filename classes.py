import sqlite3 as sql
from datetime import date
from PyQt5.QtWidgets import QLineEdit ,QPushButton ,QBoxLayout ,QApplication, QWidget, QLabel, QGridLayout, QMessageBox, QCalendarWidget, QComboBox
class SQL_SINGLE_INSTANCE:
    def __init__(self) -> None:
        self.connection = sql.connect("FINANCE_DB.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS transactions (idCategory INTEGER , idOfOther INTEGER, date DATE, money FLOAT, isIncome BOOL)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS people (idOfOther INTEGER PRIMARY KEY AUTOINCREMENT, firstName varchar(255), lastName varchar(255))")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS categories (idCategory INTEGER PRIMARY KEY AUTOINCREMENT, name varchar(255), RGB varchar(11))")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS settings (height INTEGER, width INTEGER, recordsShown INTEGER)")
        self.connection.commit()

class transaction():
    def __init__(self, date: date, money: float, idcategry: int, income: bool, idoftheother: int) -> None:
        super().__init__()
        self.idCategory = idcategry
        self.idOfOther = idoftheother
        self.date = date
        self.money = money
        self.isIncome = income

class person():
    def __init__(self, idoftheother: int, firstname: str, lastname: str) -> None:
        super().__init__()
        self.idOfOther = idoftheother
        self.firstName = firstname
        self.lastName = lastname

class category():
    def __init__(self, idcategry: int, name: str, rgb: str) -> None:
        super().__init__()
        self.idCategory = idcategry
        self.name = name
        self.rgb = rgb

class CORE(SQL_SINGLE_INSTANCE):
    def __init__(self):
        super().__init__()
        self.filters = dict()
        self.shownContent = list()

    def create_new_category(self, category: category) -> None:
        self.cursor.execute(f"INSERT INTO categories VALUES (NULL, ?, ?)", (category.name, category.rgb))
        self.connection.commit()
    
    def create_new_person(self, person: person) -> None:
        self.cursor.execute(f"INSERT INTO people VALUES (NULL, ?, ?)", (person.firstName, person.lastName))
        self.connection.commit()

    def create_new_transaction(self, transaction: transaction) -> None:
        self.cursor.execute(f"INSERT INTO transactions VALUES (?, ?, ?, ?, ?)", (transaction.idCategory, transaction.idOfOther, transaction.date, transaction.money, transaction.isIncome))
        self.connection.commit()
        
    def show_table(self, filters: dict, orderFilters: list,  limit: int) -> None:
        command = "SELECT people.firstName, people.lastName, categories.name, transactions.money, transactions.date FROM transactions LEFT JOIN categories ON transactions.idCategory = categories.idCategory LEFT JOIN people ON transactions.idOfOther = people.idOfOther "
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

        #declaring functions in advance    
        #setting the layout to grid
        g = QGridLayout()
        self.recordBox = QLineEdit(self)
        self.recordBox.setMaxLength(3)
        self.recordBox.textChanged.connect(self.change_record_num)
        g.addWidget(self.recordBox, 0, 0)
        g.addWidget(QLabel("wykres", self), 0, 1)
        g.addWidget(QLabel("imie", self), 1, 0)
        g.addWidget(QLabel("nazwisko", self), 1, 1)
        g.addWidget(QLabel("kategoria", self), 1, 2)
        g.addWidget(QLabel("kasa", self), 1, 3)
        g.addWidget(QLabel("data", self), 1, 4)
        counter = 2
        self.show_table({}, [], self.settings['rowNumber'])
        for record in self.shownContent:
            for i in range(len(record)):
                g.addWidget(QLabel(str(record[i]), self), counter, i)
            counter += 1
        self.setLayout(g)
        #window type functions, and code lines
        
        self.setGeometry(100, 100, self.settings["width"], self.settings["height"])
        self.show()

    #functions controlling all the onclicks, textchanged and so on
    
    def change_record_num(self, text) -> None:
        text = self.recordBox.text()
        try:
            text = int(text)
            self.settings['rowNumber'] = text
            self.cursor.execute("DELETE FROM settings WHERE 1=1")
            self.cursor.execute("INSERT INTO settings VALUES (?, ?, ?)", (self.settings['height'], self.settings['width'], num))
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
        super().resizeEvent(event)