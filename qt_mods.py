from PyQt5.QtCore import QSize
from PyQt5.QtGui import QColor, QPen, QPaintEvent
from PyQt5.QtWidgets import QLabel
from PyQt5 import QtCore, QtGui


class VerticalLabel(QLabel):
    def __init__(self, text):
        QLabel.__init__(self)
        self.text = text

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.translate(15, self.height()-40)
        painter.rotate(-90)
        if self.text:
            painter.drawText(0, 0, self.text)
        painter.end()

    def setText(self, text):
        self.text = text

    def minimumSizeHint(self):
        size = QLabel.minimumSizeHint(self)
        return QSize(size.height(), size.width())

    def sizeHint(self):
        size = QLabel.sizeHint(self)
        return QSize(size.height(), size.width())