from ui_confirm_dialog import Ui_Dialog
from PyQt5.QtWidgets import QDialog
from PyQt5 import QtCore


class ConfirmDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setModal(True)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        #self.setGeometry(0, 0, self.width(), self.height())
        self.btnCancelar.pressed.connect(self.btn_anular_pressed)
        self.btnAceptar.pressed.connect(self.btn_confirmar_pressed)

    def btn_anular_pressed(self):
        self.reject()

    def btn_confirmar_pressed(self):
        self.accept()