from PyQt5.QtWidgets import QWidget, QGridLayout, QScrollArea, QListWidget, QLineEdit
from PyQt5.QtCore import QDate, Qt, pyqtSignal
from PyQt5.QtGui import QPen, QPainter, QColor

class QListFilter(QWidget):
    def __init__(self, parent = None, qListValues = []) -> None:
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
        self.accesibleLayout.addWidget(self.qLabelPart, 0, 0)
        self.accesibleLayout.addWidget(self.qScrollPart, 1, 0)
        
        self.setLayout(self.accesibleLayout)

class QColorLineWidget(QWidget):
    def __init__(self, min: int, max: int):
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
        pen.setColor(Qt.black)
        painter.setPen(pen)
        painter.drawLine(0, self.height() // 2, start_pos, self.height() // 2)
        painter.drawLine(end_pos, self.height() // 2, width, self.height() // 2)

    def set_line_ratios(self, start_ratio, end_ratio):
        self.start_ratio = start_ratio
        self.end_ratio = end_ratio
        self.update()

class QFromToFilter(QWidget):
    def __init__(self, max, min, parent=None) -> None:
        super().__init__()
        self.accesibleLayout = QGridLayout()

        self.smallerData = QLineEdit()
        self.smallerData.setPlaceholderText('...Od')
        self.smallerData.textChanged.connect(self.update_color_line)

        self.biggerData = QLineEdit()
        self.biggerData.setPlaceholderText('Do...')
        self.biggerData.textChanged.connect(self.update_color_line)

        self.DataPresentationLevel = QColorLineWidget()

        self.accesibleLayout = QGridLayout()
        self.accesibleLayout.addWidget(self.DataPresentationLevel, 0, 0, 1, 2)
        self.accesibleLayout.addWidget(self.smallerData, 1, 0)
        self.accesibleLayout.addWidget(self.biggerData, 1, 1)

        self.setLayout(self.accesibleLayout)

    def update_color_line(self):
        try:
            start_ratio = float(self.startInput.text())
            end_ratio = float(self.endInput.text())
            if 0 <= start_ratio <= end_ratio <= 1:
                self.colorLineWidget.set_line_ratios(start_ratio, end_ratio)
        except ValueError:
            pass  # Ignore invalid input
