# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'newSession.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_newDialog(object):
    def setupUi(self, newDialog):
        newDialog.setObjectName("newDialog")
        newDialog.resize(400, 112)
        self.buttonBox = QtWidgets.QDialogButtonBox(newDialog)
        self.buttonBox.setGeometry(QtCore.QRect(300, 40, 81, 241))
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.labelSessionName = QtWidgets.QLabel(newDialog)
        self.labelSessionName.setGeometry(QtCore.QRect(35, 40, 99, 25))
        self.labelSessionName.setObjectName("labelSessionName")
        self.lineSessionName = QtWidgets.QLineEdit(newDialog)
        self.lineSessionName.setGeometry(QtCore.QRect(140, 40, 132, 25))
        self.lineSessionName.setObjectName("lineSessionName")

        self.retranslateUi(newDialog)
        self.buttonBox.accepted.connect(newDialog.accept)
        self.buttonBox.rejected.connect(newDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(newDialog)

    def retranslateUi(self, newDialog):
        _translate = QtCore.QCoreApplication.translate
        newDialog.setWindowTitle(_translate("newDialog", "D2R Run Tracker - New Session"))
        self.labelSessionName.setToolTip(_translate("newDialog", "Name to be used for storage purposes"))
        self.labelSessionName.setText(_translate("newDialog", "Session Name:"))
        self.lineSessionName.setStatusTip(_translate("newDialog", "Default is current date"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    newDialog = QtWidgets.QDialog()
    ui = Ui_newDialog()
    ui.setupUi(newDialog)
    newDialog.show()
    sys.exit(app.exec_())
