import sqlite3 as sql
from datetime import date

# classes which provide better handling of data from the database (data in the database has exact same syntax)
# objects with every atribute of a transaction from the database...
class transaction():
    def __init__(self, date: date, money: float, idcategry: int, idoftheother: int) -> None:
        super().__init__()
        self.idCategory = idcategry
        self.idOfOther = idoftheother
        self.date = date
        self.money = money

# ...with every atribute of the person from people table...
class person():
    def __init__(self, idoftheother: int, personName: str) -> None:
        super().__init__()
        self.idOfOther = idoftheother
        self.personName = personName

# ...and with every atribute of the category from categories table.
class category():
    def __init__(self, idcategry: int, name: str, rgb: str) -> None:
        super().__init__()
        self.idCategory = idcategry
        self.name = name
        self.rgb = rgb

# a handle for other classes to contact with the db
class SQL_SINGLE_INSTANCE:
    def __init__(self) -> None:
        self.connection = sql.connect("FINANCE_DB.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS transactions (idCategory INTEGER , idOfOther INTEGER, date DATE, money REAL)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS people (idOfOther INTEGER PRIMARY KEY AUTOINCREMENT, personName varchar(255))")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS categories (idCategory INTEGER PRIMARY KEY AUTOINCREMENT, name varchar(255), RGB varchar(11))")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS settings (height INTEGER, width INTEGER, recordsShown INTEGER)")
        self.connection.commit()
    
    def create_new_category(self, category: category) -> None:
        self.cursor.execute(f"INSERT INTO categories VALUES (NULL, ?, ?)", (category.name, category.rgb))
        self.connection.commit()
    
    def create_new_person(self, person: person) -> None:
        self.cursor.execute(f"INSERT INTO people VALUES (NULL, ?)", (person.personName))
        self.connection.commit()

    def create_new_transaction(self, transaction: transaction) -> None:
        self.cursor.execute(f"INSERT INTO transactions VALUES (?, ?, ?, ?)", (transaction.idCategory, transaction.idOfOther, transaction.date, transaction.money))
        self.connection.commit()

    