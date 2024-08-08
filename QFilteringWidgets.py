from PyQt5.QtWidgets import QWidget, QGridLayout, QScrollArea, QListWidget, QLineEdit, QComboBox, QVBoxLayout, QDateEdit
from PyQt5.QtCore import QDate, Qt, pyqtSignal
from PyQt5.QtGui import QPen, QPainter, QColor
from datetime import date

class QListFilter(QWidget):
    def __init__(self, qListValues, parent = None) -> None:
        super().__init__()
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
        self.accesibleLayout.addWidget(self.qScrollPart, 0, 0)
        
        self.setLayout(self.accesibleLayout)

class QColorLineWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.color = QColor(64, 255, 100)
        self.start_ratio = 0  # Initial start position ratio (0.0 to 1.0)
        self.end_ratio = 1 # Initial end position ratio (0.0 to 1.0)

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen()
        pen.setWidth(5)

        width = self.width()

        start_pos = int(self.start_ratio * width)
        end_pos = int(self.end_ratio * width)

        # Draw colored segment
        pen.setColor(self.color)
        painter.setPen(pen)
        painter.drawLine(start_pos, self.height() // 2, end_pos, self.height() // 2)

        # Draw the rest of the line in black
        pen.setColor(QColor(0, 100, 100))
        painter.setPen(pen)
        painter.drawLine(0, self.height() // 2, start_pos, self.height() // 2)
        painter.drawLine(end_pos, self.height() // 2, width, self.height() // 2)

    def set_line_ratios(self, start_ratio, end_ratio):
        self.start_ratio = start_ratio
        self.end_ratio = end_ratio
        self.update()

class QFromToFilter(QWidget):
    def __init__(self, max: float, min: float) -> None:
        super().__init__()
        self.accesibleLayout = QGridLayout()

        if isinstance(max, int) and isinstance(min, int):
            self.flag = int(0)
            if abs(min) != min or abs(max) != max:
                self.ratioDivider = abs(min) + abs(max)
            else:
                self.ratioDivider = float(max - min)
            self.maxValue = max
            self.minValue = min
            
            self.smallerData = QLineEdit()
            self.smallerData.setPlaceholderText('...Od')
            self.smallerData.textChanged.connect(self.update_color_line)

            self.biggerData = QLineEdit()
            self.biggerData.setPlaceholderText('Do...')
            self.biggerData.textChanged.connect(self.update_color_line)

        if isinstance(min, date) and isinstance(max, date):
            self.flag = date(2000, 2, 2)
            self.minValue = min.toordinal()
            self.maxValue = max.toordinal()
            self.ratioDivider = float(self.maxValue - self.minValue)

            self.smallerData = QDateEdit()
            self.smallerData.setDate(min)
            self.smallerData.dateChanged.connect(self.update_color_line)

            self.biggerData = QDateEdit()
            self.biggerData.setDate(max)
            self.biggerData.dateChanged.connect(self.update_color_line)

        self.DataPresentationLevel = QColorLineWidget()

        self.accesibleLayout = QGridLayout()
        self.accesibleLayout.addWidget(self.DataPresentationLevel, 0, 0, 1, 2)
        self.accesibleLayout.addWidget(self.smallerData, 1, 0)
        self.accesibleLayout.addWidget(self.biggerData, 1, 1)

        self.setLayout(self.accesibleLayout)

    def update_color_line(self):
        try:
            if self.flag == int(0):
                start_ratio = float(self.smallerData.text())/self.ratioDivider
                end_ratio = (float(self.biggerData.text())-self.minValue)/self.ratioDivider
            elif self.flag == date(2000, 2, 2):
                try:
                    print(f'tutaj! {self.i+1}')
                    self.i += 1
                except:
                    self.i = 0
                start_ratio = float(self.smallerData.date().toPyDate().toordinal()-self.minValue-1)/self.ratioDivider
                end_ratio = float(self.biggerData.date().toPyDate().toordinal()-self.minValue)/self.ratioDivider
                print(start_ratio, self.ratioDivider)
            if 0 <= start_ratio <= end_ratio <= 1:
                self.DataPresentationLevel.set_line_ratios(start_ratio, end_ratio)
        except ValueError:
            pass  # Ignore invalid input

class QFTLFilter(QWidget):
    def __init__(self, max, min) -> None:
        super().__init__()
        self.qComboComponent = QComboBox()
        self.qComboComponent.addItems(['Zakres', 'Konkretne wartości'])
        self.qComboComponent.currentIndexChanged.connect(self.on_val_changed)

        self.currentFilter = [QFromToFilter(max, min), QListFilter(qListValues=[])]

        self.accesibleLayout = QVBoxLayout()
        self.populate_grid(self.accesibleLayout)
        self.setLayout(self.accesibleLayout)

    def on_val_changed(self) -> None:
        print(self.qComboComponent.currentIndex())

    def populate_grid(self, layout: QVBoxLayout) -> None:
        layout.addWidget(self.qComboComponent)
        layout.addWidget(self.currentFilter[self.qComboComponent.currentIndex()])
        