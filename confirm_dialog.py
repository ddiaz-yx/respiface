from PyQt5.QtGui import QMouseEvent

from ui_confirm_dialog import Ui_Dialog
from PyQt5.QtWidgets import QDialog
from PyQt5 import QtCore
import styles as st
from functools import partial


class ConfirmDialog(QDialog, Ui_Dialog):

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setModal(True)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        #self.setGeometry(0, 0, self.width(), self.height())
        self.frm_yes.mousePressEvent = partial(self.frm_yes_pressed)
        self.frm_no.mousePressEvent = partial(self.frm_no_pressed)
        self.set_styles()
        self.setCursor(QtCore.Qt.BlankCursor)

    def set_styles(self):
        self.setStyleSheet("background-color: black")
        self.frm_yes.setStyleSheet(st.qss_frm_top)
        self.frm_no.setStyleSheet(st.qss_frm_top)

    def frm_no_pressed(self, event: QMouseEvent):
        self.reject()

    def frm_yes_pressed(self, event: QMouseEvent):
        self.accept()
