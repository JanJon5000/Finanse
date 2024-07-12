import sqlite3 as sql
from datetime import date
from PyQt5.QtWidgets import QLineEdit ,QPushButton ,QBoxLayout ,QApplication, QWidget, QLabel, QGridLayout, QMessageBox, QCalendarWidget, QComboBox, QMainWindow
class SQL_SINGLE_INSTANCE:
    def __init__(self) -> None:
        self.connection = sql.connect("FINANCE_DB.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS transactions (idCategory INTEGER , idOfOther INTEGER, date DATE, money FLOAT, isIncome BOOL)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS people (idOfOther INTEGER PRIMARY KEY AUTOINCREMENT, firstName varchar(255), lastName varchar(255))")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS categories (idCategory INTEGER PRIMARY KEY AUTOINCREMENT, name varchar(255), RGB varchar(11))")
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

class mainWind(SQL_SINGLE_INSTANCE):
    def __init__(self):
        super().__init__()
        self.filters = dict()
        self.shownContent = tuple()

    def create_new_category(self, category: category) -> None:
        self.cursor.execute(f"INSERT INTO categories VALUES (NULL, ?, ?)", (category.name, category.rgb))
        self.connection.commit()
    
    def create_new_person(self, person: person) -> None:
        self.cursor.execute(f"INSERT INTO people VALUES (NULL, ?, ?)", (person.firstName, person.lastName))
        self.connection.commit()

    def create_new_transaction(self, transaction: transaction) -> None:
        self.cursor.execute(f"INSERT INTO transactions VALUES (?, ?, ?, ?, ?)", (transaction.idCategory, transaction.idOfOther, transaction.date, transaction.money, transaction.isIncome))
        self.connection.commit()
        
    def show_table(self, filt: dict) -> None:
        command = "SELECT people.firstName, people.lastName, categories.name, transactions.money, transactions.date FROM transactions FULL JOIN categories, people ON (transactions.idCategory = categories.idCategory AND transactions.idOfOther = people.idOfOther)"
        self.filters = filt
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
        print(command)
        self.cursor.execute(command)
        self.shownContent = self.cursor.fetchall()
        print(self.shownContent)