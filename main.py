from ProgramClass import transaction, person, category, CORE, Program
from datetime import date, datetime
from PyQt5.QtWidgets import QApplication
from sys import argv, exit

if __name__ == "__main__":
    app = QApplication(argv)
    widget = Program()
    exit(app.exec_())
