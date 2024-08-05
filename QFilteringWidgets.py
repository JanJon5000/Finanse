from PyQt5.QtWidgets import QWidget, QGridLayout, QScrollArea, QListWidget, QLabel, QDialog, QVBoxLayout, QDateEdit, QSlider, QHBoxLayout
from PyQt5.QtCore import QDate, Qt, pyqtSignal

class QListFilter(QWidget):
    def __init__(self, parent = None, qListValues = [], name = "") -> None:
        super().__init__()

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

class QDateRangePicker(QWidget):
    def __init__(self):
        super().__init__()

        self.start_date_edit = QDateEdit(self)
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.setDate(QDate.currentDate().addDays(-30))

        self.end_date_edit = QDateEdit(self)
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.setDate(QDate.currentDate())

        with open("styleSHEETS/callendar-stylesheet.qss", "r") as file:
            for i in [self.end_date_edit, self.start_date_edit]:
                qss = file.read()
                i.setStyleSheet(qss)

        self.start_date_edit.dateChanged.connect(self.update_range)
        self.end_date_edit.dateChanged.connect(self.update_range)

        layout = QVBoxLayout()
        layout.addWidget(self.start_date_edit)
        layout.addWidget(self.end_date_edit)

        self.setLayout(layout)

    def update_range(self):
        if self.start_date_edit.date() > self.end_date_edit.date():
            self.start_date_edit.setDate(self.end_date_edit.date())

class QMoneyRangeSlider(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumWidth(300)
        
        self.lower_slider = QSlider(Qt.Horizontal)
        self.lower_slider.setRange(0, 100)
        self.lower_slider.setValue(20)
        
        self.upper_slider = QSlider(Qt.Horizontal)
        self.upper_slider.setRange(0, 100)
        self.upper_slider.setValue(80)
        
        self.lower_slider.valueChanged.connect(self.update_range)
        self.upper_slider.valueChanged.connect(self.update_range)

        layout = QVBoxLayout()
        layout.addWidget(self.lower_slider)
        layout.addWidget(self.upper_slider)
        
        self.range_label = QLabel(self.get_range_text())
        layout.addWidget(self.range_label)

        self.setLayout(layout)
        
    def update_range(self):
        if self.lower_slider.value() > self.upper_slider.value():
            self.lower_slider.setValue(self.upper_slider.value())

    def get_range_text(self):
        return f"Range: {self.lower_slider.value()} - {self.upper_slider.value()}"

class QFilterBoxWidget(QDialog):
    closed = pyqtSignal()
    def __init__(self, parent=None) -> None:
        super().__init__()
        QDialog.__init__(parent)
        self.accesibleLayout = QHBoxLayout()
        self.widgetList = [QListFilter(qListValues=[], name="Imie"), 
                           QListFilter(qListValues=[], name="Kategoria"),
                           QDateRangePicker(),
                           QMoneyRangeSlider()
                          ]
        for widg in self.widgetList:
            self.accesibleLayout.addWidget(widg)
        self.setLayout(self.accesibleLayout)

    def closeEvent(self, event) -> None:
        self.closed.emit()
        super().closeEvent(event)