from PyQt5.QtWidgets import QWidget, QGridLayout, QScrollArea, QListWidget, QLineEdit, QComboBox, QSizePolicy, QVBoxLayout, QDateEdit, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtCore import QDate, Qt, pyqtSignal  
from PyQt5.QtGui import QFocusEvent, QMouseEvent, QPen, QPainter, QColor, QDoubleValidator
from datetime import date

class QListFilter(QWidget):
    def __init__(self, qListValues) -> None:
        # initializer of the parent class
        super().__init__()
        self.qScrollPart = QScrollArea(self)
        self.content = [str(i) for i in qListValues]
        # customizing scrollable part - a list with items to be displayed - a user chooses
        self.qScrollPart.setWidgetResizable(True)
        self.qListPart = QListWidget()
        self.qListPart.addItems(self.content)
        self.qListPart.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # user can select multiple
        self.qListPart.setSelectionMode(QListWidget.ExtendedSelection)

        self.qScrollPart.setWidget(self.qListPart)

        # a fixed layout of the widget
        self.accesibleLayout = QGridLayout(self)
        self.accesibleLayout.addWidget(self.qScrollPart, 0, 0)
        
        self.setLayout(self.accesibleLayout)

    def select_items(self, values: list) -> None:
        for i in range(self.qListPart.count()):
            item = self.qListPart.item(i)
            if item.text() in values:
                item.setSelected(True)
        self.update()
        

class QColorLineWidget(QWidget):
    def __init__(self):
        # a line-object that changes its part size that is colored with a function
        super().__init__()
        # colored part will be in this color
        self.color = QColor(0, 0, 255)
        self.start_ratio = 0  # Initial start position ratio (0.0 to 1.0)
        self.end_ratio = 1 # Initial end position ratio (0.0 to 1.0)

    # overwritten function of paintEvent which ocurs when the object is painted (displayed) 
    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen()
        pen.setWidth(5)

        width = self.width()

        start_pos = int(self.start_ratio * width)
        end_pos = int(self.end_ratio * width)

        # draw colored segment
        pen.setColor(self.color)
        painter.setPen(pen)
        painter.drawLine(start_pos, self.height() // 2, end_pos, self.height() // 2)

        # draw the rest of the line in this color
        pen.setColor(QColor(255, 255, 255))
        painter.setPen(pen)
        painter.drawLine(0, self.height() // 2, start_pos, self.height() // 2)
        painter.drawLine(end_pos, self.height() // 2, width, self.height() // 2)

    # function that changes the size of colored fragment
    def set_line_ratios(self, start_ratio, end_ratio):
        self.start_ratio = start_ratio
        self.end_ratio = end_ratio
        self.update()

class QFromToFilter(QWidget):
    def __init__(self, max: float, min: float) -> None:
        # a filter that can filer data in a range - if the user wants data from X value to Y value, they will use this
        super().__init__()
        # its layout
        self.accesibleLayout = QGridLayout()
        self.negativeAlertFlag = False
        self.maxMinRange = True

        # two cases - date and a number (only those things in my program require that filter to exist)
        if isinstance(max, float) and isinstance(min, float):
            # this syntax is totally unnecesary - i still decided to write it like this, so i would instantly recognize what this is for
            self.flag = int(0)
            # value of a transaction can be negative when it is from the user to someone - thats where abs value comes into play to determine how to create boundaries in the widget
            if abs(min) != min or abs(max) != max:
                self.ratioDivider = abs(min) + abs(max)
                self.negativeAlertFlag = True
            else:
                self.ratioDivider = float(max - min)
            self.maxValue = max
            self.minValue = min
            
            # lineedits since this is for numbers for the start of the range...
            self.smallerData = QLineEdit()
            self.smallerData.setValidator(QDoubleValidator(self.minValue, self.maxValue, 2))
            self.smallerData.setPlaceholderText('Od...')
            self.smallerData.textChanged.connect(self.update_color_line)

            # ... and for the end of the range
            self.biggerData = QLineEdit()
            self.smallerData.setValidator(QDoubleValidator(self.minValue, self.maxValue, 2))
            self.biggerData.setPlaceholderText('...Do')
            self.biggerData.textChanged.connect(self.update_color_line)
            
            self.labels = [QLabel(str(self.minValue)), QLabel(str(self.maxValue))]
            
        # date case
        if isinstance(min, date) and isinstance(max, date):
            # flag variable for later
            self.flag = date(2000, 2, 2)
            self.labels = [QLabel(str(min)), QLabel(str(max))]
            # cast it to a number
            self.minValue = min.toordinal()
            self.maxValue = max.toordinal()
            self.ratioDivider = float(self.maxValue - self.minValue)

            # date edits to enter a start of a range and an end of one
            self.smallerData = QDateEdit()
            self.smallerData.setMaximumDate(max)
            self.smallerData.setMinimumDate(min)
            self.smallerData.setDate(min)
            self.smallerData.dateChanged.connect(self.update_color_line)
            self.smallerData.setDisplayFormat('yyyy-MM-dd')
            
            self.biggerData = QDateEdit()
            self.biggerData.setMaximumDate(max)
            self.biggerData.setMinimumDate(min)
            self.biggerData.setDate(max)
            self.biggerData.dateChanged.connect(self.update_color_line)
            self.biggerData.setDisplayFormat('yyyy-MM-dd')

        # variable able to graphically represent the range
        self.DataPresentationLevel = QColorLineWidget()
        self.DataPresentationLevel.setMinimumHeight(10)
        
        self.labels[0].setObjectName('range')
        self.labels[1].setObjectName('range')
        self.biggerData.setObjectName('edit')
        self.smallerData.setObjectName('edit')
        # a layout of the widget
        self.accesibleLayout = QGridLayout()
        self.accesibleLayout.addWidget(self.labels[0], 0, 0)
        self.accesibleLayout.addWidget(self.labels[1], 0, 3)
        self.accesibleLayout.addWidget(self.DataPresentationLevel, 1, 0, 1, 4)
        self.accesibleLayout.addWidget(self.smallerData, 2, 0, 1, 2)
        self.accesibleLayout.addWidget(self.biggerData, 2, 2, 1, 2)

        self.setLayout(self.accesibleLayout)

    def update_color_line(self):
        # function changing the color coverage
        try:
            if self.flag == int(0):
                if self.smallerData.text() != '' and self.biggerData.text() != '':
                    smaller_value = float(self.smallerData.text())
                    bigger_value = float(self.biggerData.text())
                elif self.smallerData.text() == '' and self.biggerData.text() != '':
                    smaller_value = self.minValue
                    bigger_value = float(self.biggerData.text())
                elif self.smallerData.text() != '' and self.biggerData.text() == '':
                    smaller_value = float(self.smallerData.text())
                    bigger_value = self.maxValue
                elif self.smallerData.text() == '' and self.biggerData.text() == '':
                    smaller_value = self.minValue
                    bigger_value = self.maxValue
                if smaller_value >= 0 and bigger_value >= 0:
                    # both inputs are positive
                    start_ratio = (smaller_value - self.minValue) / self.ratioDivider
                    end_ratio = (bigger_value - self.minValue) / self.ratioDivider
                elif smaller_value < 0 and bigger_value < 0:
                    # both negative
                    start_ratio = abs(smaller_value - self.minValue) / self.ratioDivider
                    end_ratio = abs(bigger_value - self.minValue) / self.ratioDivider
                elif smaller_value < 0 < bigger_value:
                    # one negative one positive
                    start_ratio = (smaller_value - self.minValue) / self.ratioDivider
                    end_ratio = (bigger_value - self.minValue) / self.ratioDivider
                
            elif self.flag == date(2000, 2, 2):
                start_ratio = float(self.smallerData.date().toPyDate().toordinal()-self.minValue)/self.ratioDivider
                end_ratio = float(self.biggerData.date().toPyDate().toordinal()-self.minValue)/self.ratioDivider
            if 0 <= start_ratio <= end_ratio <= 1:
                self.DataPresentationLevel.set_line_ratios(start_ratio, end_ratio)
        except ValueError:
            pass  # Ignore invalid input
    
    def select_items(self, values: list) -> None:
        try:
            self.smallerData.setText(values[0])
            self.biggerData.setText(values[1])
        except:
            self.smallerData.setDate(values[0])
            self.biggerData.setDate(values[1])

class QFTLFilter(QWidget):
    # a filter class combining the two QFromToFilter and QListFilter - for date and money filtering purposes
    def __init__(self, max: float, min: float, listOfValues: list, state: bool, reload=False) -> None:
        super().__init__()
        # a layout of the widget
        self.accesibleLayout = QVBoxLayout()
        # variables for later use so the widget wont bug/crush
        self.forLaterVals = [max, min, listOfValues]
        self.flag = state

        self.populate_grid()
        
        self.setLayout(self.accesibleLayout)
        
    def populate_grid(self) -> None:
        # function filling up the grid of the widget
        self.qComboComponent = QComboBox()
        # a combobox which by the user chooses which filter widget they want to filter the data with
        self.qComboComponent.addItems(['Zakres', 'Konkretne wartości'])
        self.qComboComponent.setCurrentIndex(self.flag)
        self.qComboComponent.currentIndexChanged.connect(self.refresh)
        
        self.currentFilter = [QFromToFilter(self.forLaterVals[0], self.forLaterVals[1]), QListFilter(qListValues=self.forLaterVals[2])]
        self.accesibleLayout.addWidget(self.qComboComponent)
        self.accesibleLayout.addWidget(self.currentFilter[self.flag])

    def refresh(self) -> None:
        # function that refreshes the grid
        self.flag = not self.flag
        self.clear_layout(self.accesibleLayout)
        self.populate_grid()
        self.update()
    
    def clear_layout(self, layout):
        if layout is not None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget() is not None:
                    child.widget().deleteLater()
                elif child.layout() is not None:
                    self.clear_layout(child.layout())

