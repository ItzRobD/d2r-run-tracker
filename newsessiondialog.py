# Copyright (C) 2021 - Rob Durst
# This file is a part of D2R Run Tracker
#
# D2R Run Tracker is free software. You may redistribute and/or modify it under the terms
# of the GNU General Public License as published by the Free Software Foundation, either
# as version 3 of the License, or (at your option) any later version. See the
# GNU General Public License for more details.
#
# D2R Run Tracker is being distributed in the hope that it will be useful and helpful
# for Diablo 2 Resurrected players but WITHOUT ANY WARRANTY. This software is NOT
# supported by Blizzard Entertainment in any way. This software does NOT interact
# with any other software of game engines and requires manual input

import logging
import os
from pathlib import Path
from os.path import exists as file_exists
from PyQt5 import QtCore, QtGui, QtWidgets
from newdialog import Ui_newDialog
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QRegExp
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QPushButton

class NewSessionDialog(QtWidgets.QDialog, Ui_newDialog):
    def __init__(self):
        super(NewSessionDialog, self).__init__()
        self.setupUi(self)

        self.setFixedSize(400, 112)
        self.setWindowTitle("D2R Run Tracker - New session")

        # Sets up input validation for lineSessionName
        # Alphanumeric and _
        # Max length 15
        self.lineSessionName.setValidator(QRegExpValidator(QRegExp(r'\w+')))
        self.lineSessionName.setMaxLength(15)

        date = QDate.currentDate()
        default_name = "%d_%d_%d" % (date.year(), date.month(), date.day())
        self.lineSessionName.setText(default_name)

    def closeEvent(self, event):
        print("X Pressed")
        self.accept()
        super().closeEvent(event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            return

    def accept(self):
        saved_sessions_path = Path("saved/sessions")
        # First check to see if the directory exists, if not create it
        if not saved_sessions_path.exists():
            Path(saved_sessions_path).mkdir(parents=True, exist_ok=True)
        # If the input field is left blank we have to create a file name for the user defaulting to the date
        if not self.lineSessionName.text():
            date = QDate.currentDate()
            default_name = "%d_%d_%d" % (date.year(), date.month(), date.day())
            # We must check to see if that file already exists and if so append a new number to it
            if not saved_sessions_path.exists():
                Path(saved_sessions_path).mkdir(parents=True, exist_ok=True)
            if file_exists(str(saved_sessions_path) + "/" + self.lineSessionName.text() + ".json"):
                number_to_append = 0
                for filename in os.listdir("saved/sessions"):
                    if filename.endswith(".json") and filename.startswith(default_name):
                        number_to_append += 1
                        if number_to_append > 9999:
                            number_to_append = 1
                default_name += "_"+str(number_to_append).zfill(4)
        else:
            # We must check to see if that file already exists and if so append a new number to it
            if file_exists(str(saved_sessions_path) + "/" + self.lineSessionName.text() + ".json"):
                number_to_append = 0
                for filename in os.listdir("saved/sessions"):
                    if filename.endswith(".json") and filename.startswith(self.lineSessionName.text()):
                        number_to_append += 1
                        if number_to_append > 9999:
                            number_to_append = 1
                save_name = self.lineSessionName.text() + "_" + str(number_to_append).zfill(4)
                self.lineSessionName.setText(save_name)

        super().accept()

    def getInput(self):
        if self.exec_() == QtWidgets.QDialog.Accepted:
            string = self.lineSessionName.text()
            return string
        else:
            return None


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog = NewSessionDialog()
