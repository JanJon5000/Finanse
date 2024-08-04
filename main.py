from ProgramClass import transaction, person, category, CORE, Program
from datetime import date, datetime
from PyQt5.QtWidgets import QApplication
from sys import argv, exit

if __name__ == "__main__":
    app = QApplication(argv)
    with open("program_stylesheet.qss", "r") as file:
        qss = file.read()
        app.setStyleSheet(qss)
    widget = Program()
    exit(app.exec_())

# To do
# wyswietlanie sie negatywnych kwot w widoku głównym, kategorii w kolorach
# QDialog filtrów