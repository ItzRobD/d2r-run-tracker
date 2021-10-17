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

__version__ = "0.6"

import os
import base64
import json
import webbrowser
import logging
from pathlib import Path
from PyQt5 import QtCore, QtGui, QtWidgets
from runtrackerv02 import Ui_MainWindow
from newsessiondialog import NewSessionDialog
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QIcon
from os.path import exists as file_exists
from prettytable import PrettyTable
from copy import deepcopy

compatible_versions = {"0.6"}

logging.basicConfig(level=logging.INFO, filename="tracker.log")
logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("tracker.log", mode="w")
formatter = logging.Formatter("%(asctime)s : %(levelname)s : %(name)s : %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.propagate = False

class d2runtracker(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(d2runtracker, self).__init__()
        self.setupUi(self)
        # Prevent window from being resized
        self.setFixedSize(854, 738)
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        # Variables
        # used for displaying the run number in labelSessionRunNumberCounter
        self.current_run_number = 1
        self.current_run_name = str()

        # item_set_list is a plaintext list of set items
        item_set_list = self.populateSetList()
        # item_uniques_list is a plaintext list of unique items
        item_uniques_list = self.populateUniquesList()
        # rune_list is a plaintext list of runes
        rune_list = self.populateRuneList()

        # initalize the found item list - is used to hold char data and item data
        self.found_item_list = list()

        # Called immediately to prompt the user to choose a session name
        self.newSession()

        # MENU
        # ### FILE
        # New
        self.actionNew_Session.triggered.connect(self.newSession)
        # Restore Backup
        self.actionRestore_Runs.triggered.connect(self.restoreRuns)
        # Open
        self.actionOpen_Session.triggered.connect(self.openSession)
        # Exit
        self.actionExit.triggered.connect(self.exitApp)
        # #### CURRENT SESSION
        # Complete session
        self.actionComplete_Session.triggered.connect(self.completeSession)
        # Generate report
        self.actionGenerate_Report.triggered.connect(self.generateReport)
        # #### HELP
        # Manual
        self.actionManual.triggered.connect(self.openManual)
        # About
        self.actionAbout.triggered.connect(self.displayAboutWindow)

        # GROUP - Item
        # Populate the combo boxes for set, unique, and runes
        self.comboItemType.addItem("Uniques", item_uniques_list)
        self.comboItemType.addItem("Sets", item_set_list)
        self.comboItemType.addItem("Runes", rune_list)
        # Whenever a user changes the item type ensure the item names change accordingly
        self.comboItemType.currentIndexChanged.connect(self.updateItemCombo)
        self.updateItemCombo(self.comboItemType.currentIndex())
        # Handle Add item button
        self.buttonItemAdd.clicked.connect(self.addItemButtonClicked)

        # GROUP - Items Found
        # Setup Found Item Table
        self.tableItemList.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableItemList.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableItemList.setColumnWidth(0, 50)
        self.tableItemList.setColumnWidth(1, 150)
        self.tableItemList.setColumnWidth(2, 50)
        self.tableItemList.setColumnWidth(3, 50)
        self.tableItemList.setColumnWidth(4, 80)
        self.tableItemList.setColumnWidth(5, 130)
        self.tableItemList.setColumnWidth(6, 80)

        # BUTTONS
        # Remove Item Button
        self.buttonRemoveItem.clicked.connect(self._removeItem)
        # Save run button
        self.buttonRunCompleted.clicked.connect(self.completeRun)
        # Generate report button
        self.buttonGenerateReport.clicked.connect(self.generateReport)
        # Complete session button
        self.buttonComplete.clicked.connect(self.completeSession)

    # Called to decode dat files and populate item lists
    def populateSetList(self):
        set_file = open("data/sets.dat", "rb").read()
        if set_file:
            set64_data = set_file
            set_data_bytes = base64.b64decode(set64_data)
            set_data_decoded = set_data_bytes.decode('ascii')
            item_set_list = list(set_data_decoded.split("\n"))
            item_set_list = item_set_list[:-1]
            logger.info("set_file loaded successfully")
            return item_set_list
        else:
            logger.critical("set_file is empty")

    def populateUniquesList(self):
        uniques_file = open("data/uniques.dat", "rb").read()
        if uniques_file:
            uniques64_data = uniques_file
            uniques_data_bytes = base64.b64decode(uniques64_data)
            uniques_data_decoded = uniques_data_bytes.decode('ascii')
            item_uniques_list = list(uniques_data_decoded.split("\n"))
            item_uniques_list = item_uniques_list[:-1]
            logger.info("uniques_file loaded successfully")
            return item_uniques_list
        else:
            logger.critical("uniques_file is empty")

    def populateRuneList(self):
        rune_file = open("data/runes.dat", "rb").read()
        if rune_file:
            rune64_data = rune_file
            rune_data_bytes = base64.b64decode(rune64_data)
            rune_data_decoded = rune_data_bytes.decode('ascii')
            rune_list = list(rune_data_decoded.split("\n"))
            rune_list = rune_list[:-1]
            logger.info("rune_file loaded successfully")
            return rune_list
        else:
            logger.critical("rune_file is empty")

    # populate the item name list according to selected item type
    def updateItemCombo(self, index):
        self.comboItemName.clear()
        items = self.comboItemType.itemData(index)
        if items:
            self.comboItemName.addItems(items)

    # called when add item is clicked
    def addItemButtonClicked(self):
        self.addItemToFoundList(__version__,
                                self.lineSessionName.text(),
                                self.getCurrentRunNumber(),
                                self.comboItemName.currentText(),
                                self.comboItemType.currentText()[0],
                                self.spinboxItemQuanity.value(),
                                self.cbItemIsEthereal.isChecked(),
                                self.getCompletionsString(),
                                self.comboSessionDifficulty.currentIndex(),
                                self.comboCharClass.currentIndex(),
                                self.spinboxCharacterLevel.value(),
                                self.spinboxCharacterMF.value(),
                                self.spinboxSessionPlayers.value(),
                                QtCore.QTime.currentTime().toString()
                                )
        self.cbItemIsEthereal.setChecked(False)

    # adds args to a dict to add to the found item list
    def addItemToFoundList(self,
                           current_version,
                           current_session,
                           current_run_number,
                           current_item_name,
                           current_item_type,
                           current_item_quantity,
                           current_item_ethereal,
                           current_completions,
                           current_difficulty,
                           current_class,
                           current_level,
                           current_mf,
                           current_players,
                           current_time
                           ):


        current_item = {"tracker_version" : __version__,
                        "session_name": current_session,
                        "run_number": current_run_number,
                        "item_name": current_item_name,
                        "item_type": current_item_type,
                        "item_quantity": current_item_quantity,
                        "item_ethereal": current_item_ethereal,
                        "completions": current_completions,
                        "difficulty": current_difficulty,
                        "class": current_class,
                        "level": current_level,
                        "mf": current_mf,
                        "players": current_players,
                        "time_found" : current_time}

        if len(self.found_item_list) > 0:
            if "total_runs" in self.found_item_list[-1]:
                self.found_item_list = self.found_item_list[:-1]

        self.found_item_list.append(current_item)

        self.updateItemsFoundTable()
        self.tableItemList.selectRow(self.tableItemList.rowCount() - 1)

    # returns the run number
    def getCurrentRunNumber(self):
        return self.current_run_number

    # set the run number to value
    def setCurrentRunNumber(self, value):
        self.current_run_number = value

    # returns the found item list
    def getFoundItemList(self):
        return self.found_item_list

    # called to ensure the found item table is updated and is properly formatted
    def updateItemsFoundTable(self):
        row = 0
        item_list = self.getFoundItemList()
        if item_list:
            difficulty_list = ["Normal", "Nightmare", "Hell"]

            self.tableItemList.setRowCount(len(item_list))
            for item in item_list:
                if "total_runs" not in item:
                    self.tableItemList.setItem(row, 0, QtWidgets.QTableWidgetItem(str(item["run_number"])))
                    contents = self.tableItemList.item(row, 0)
                    contents.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.tableItemList.setItem(row, 1, QtWidgets.QTableWidgetItem(item["item_name"]))
                    contents = self.tableItemList.item(row, 1)
                    contents.setTextAlignment(QtCore.Qt.AlignCenter)
                    if item["item_ethereal"]:
                        self.tableItemList.setItem(row, 2, QtWidgets.QTableWidgetItem("Eth"))
                        contents = self.tableItemList.item(row, 2)
                        contents.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.tableItemList.setItem(row, 3, QtWidgets.QTableWidgetItem(item["item_type"]))
                    contents = self.tableItemList.item(row, 3)
                    contents.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.tableItemList.setItem(row, 4, QtWidgets.QTableWidgetItem(str(item["item_quantity"])))
                    contents = self.tableItemList.item(row, 4)
                    contents.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.tableItemList.setItem(row, 5, QtWidgets.QTableWidgetItem(item["completions"]))
                    contents = self.tableItemList.item(row, 5)
                    contents.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.tableItemList.setItem(row, 6, QtWidgets.QTableWidgetItem(difficulty_list[item["difficulty"]]))
                    contents = self.tableItemList.item(row, 6)
                    contents.setTextAlignment(QtCore.Qt.AlignCenter)
                    row += 1
        else:
            self.tableItemList.clearContents()

    # generates the completions string based on which checkboxes are ticked
    def getCompletionsString(self):
        completions_string = str()
        if self.cbCAndariel.isChecked():
            completions_string = completions_string + "A"
        if self.cbCDuriel.isChecked():
            completions_string = completions_string + "Du"
        if self.cbCMephisto.isChecked():
            completions_string = completions_string + "M"
        if self.cbCDiablo.isChecked():
            completions_string = completions_string + "D"
        if self.cbCBaal.isChecked():
            completions_string = completions_string + "B"
        if self.cbCPindleskin.isChecked():
            completions_string = completions_string + "P"
        if self.cbCNihlathak.isChecked():
            completions_string = completions_string + "N"
        if self.cbCSummoner.isChecked():
            completions_string = completions_string + "S"
        if self.cbCCountess.isChecked():
            completions_string = completions_string + "C"
        if self.cbCCouncil.isChecked():
            completions_string = completions_string + "mc"
        if self.cbCPit.isChecked():
            completions_string = completions_string + "p"
        if self.cbCTunnels.isChecked():
            completions_string = completions_string + "ac"
        if self.cbCTravincal.isChecked():
            completions_string = completions_string + "t"
        if self.cbCCows.isChecked():
            completions_string = completions_string + "c"
        return completions_string

    # called to remove the selected row from the found item table
    def _removeItem(self):
        current_row = int()
        if self.tableItemList.currentRow() < 0:
            logger.warning("Attempting to remove a row which does not exist - returning")
            return
        else:
            current_row = self.tableItemList.currentRow()

        if self.getFoundItemList():
            self.getFoundItemList().pop(current_row)
        self.updateItemsFoundTable()

    # when called it will save an encoded .run file of the current data
    # and increment the run count
    def completeRun(self):
        # create item list
        item_list = self.getFoundItemList()
        # add last run to keep track correctly
        if "total_runs" in item_list[-1]:
            item_list = item_list[:-1]
            item_list.append({"total_runs": self.getCurrentRunNumber()})
        else:
            item_list.append({"total_runs": self.getCurrentRunNumber()})

        # encode to json
        item_list_json = self.encodeJSON(item_list)
        # encode to b64
        item_list_json_bytes = item_list_json.encode("ascii")
        encoded_json = base64.b64encode(item_list_json_bytes)
        encoded_json = encoded_json.decode("ascii")
        saved_runs_path = Path("saved/runs/")
        if not saved_runs_path.exists():
           Path("saved/runs").mkdir(parents=True, exist_ok=True)
        o = open("saved/runs/" + self.getSessionName() + ".run", "w")
        o.write(encoded_json)
        logger.info(str("Run - {0} - saved as file - {1}").format(self.getCurrentRunNumber(),
                                                                  str(saved_runs_path) + "/" + self.getSessionName()
                                                                  + ".run"))
        o.close()
        #increment run counter
        self.incrementRunNumber()

    # when called it will save a json of the current data
    # and delete any .run files which share the current session name
    # to prevent accumulating unnecessary files
    # will then begin a new session
    def completeSession(self):
        # Confirm user wants to complete the session
        confirmation_box = QMessageBox()
        confirmation_box.setIcon(QMessageBox.Information)
        confirmation_box.setWindowTitle("Complete session?")
        confirmation_box.setText("Do you want to complete the session?")
        confirmation_box.setInformativeText("WARNING: The found item list and backups will be cleared upon"
                                            " completing the session")
        confirmation_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        if confirmation_box.exec_() == QMessageBox.Cancel:
            return

        # create item list
        item_list = self.getFoundItemList()
        # add last run to keep track correctly
        item_list.append({"total_runs": self.getCurrentRunNumber()})
        # encode to json
        item_list_json = self.encodeJSON(item_list)
        # save to completed folder in plain text
        completed_session_path = Path("saved/sessions")
        if not completed_session_path.exists():
            Path(completed_session_path.mkdir(parents=True, exist_ok=True))
        o = open(str(completed_session_path) + "/" + self.getSessionName() + ".json", "w")
        o.write(item_list_json)
        logger.info(str("Session - {0} - saved as file - {1}").format(self.getSessionName(), str(completed_session_path) + "/" + self.getSessionName() + ".json"))
        o.close()

        # delete temporary run files
        saved_runs_path = Path("saved/runs/")
        if saved_runs_path.exists():
            if file_exists(str(saved_runs_path) + "/" + self.lineSessionName.text() + ".run"):
                os.remove(str(saved_runs_path) + "/" + self.lineSessionName.text() + ".run")


        # start new session
        self.newSession()

    # takes arg - data to encode to a json and returns that value
    def encodeJSON(self, data):
        data_to_encode = data
        json_encoded_data = json.dumps(data_to_encode, indent=4)
        return json_encoded_data

    # takes arg - json_data to decode to a list and returns that value
    def decodeJSON(self, json_data):
        json_to_decode = json_data
        json_data
        decoded_data = json.loads(json_to_decode)
        return decoded_data

    # increments the run number by 1
    def incrementRunNumber(self):
        self.current_run_number += 1
        self.labelSessionRunNumberCounter.setText(str(self.current_run_number))

    # returns the session name
    def getSessionName(self):
        if self.lineSessionName.text():
            return self.lineSessionName.text()
        else:
            return "unnamed"

    # starts a new session - prompts the user for a new session name and sets defaults
    def newSession(self):
        new_dialog = NewSessionDialog()
        new_session_name = new_dialog.getInput()
        if new_session_name:
            self.lineSessionName.setText(new_session_name)
            self.lineSessionName.setEnabled(False)
            self.setDefaults()

    # reset all values to default
    def setDefaults(self):
        self.spinboxSessionPlayers.setValue(1)
        self.comboSessionDifficulty.setCurrentIndex(0)
        self.setCurrentRunNumber(1)
        self.labelSessionRunNumberCounter.setText(str(self.getCurrentRunNumber()))
        self.comboCharClass.setCurrentIndex(0)
        self.spinboxCharacterLevel.setValue(1)
        self.spinboxCharacterMF.setValue(0)
        self.comboItemType.setCurrentIndex(0)
        self.comboItemName.setCurrentIndex(0)
        self.spinboxItemQuanity.setValue(0)
        self.resetAllCompletions()
        self.found_item_list.clear()
        self.tableItemList.clearContents()
        self.tableItemList.setRowCount(0)

    # toggle all checkboxes
    def toggleAllCompletions(self):
        self.cbCAndariel.toggle()
        self.cbCDuriel.toggle()
        self.cbCMephisto.toggle()
        self.cbCDiablo.toggle()
        self.cbCBaal.toggle()
        self.cbCPindleskin.toggle()
        self.cbCNihlathak.toggle()
        self.cbCSummoner.toggle()
        self.cbCCountess.toggle()
        self.cbCCouncil.toggle()
        self.cbCPit.toggle()
        self.cbCTunnels.toggle()
        self.cbCTravincal.toggle()
        self.cbCCows.toggle()

    # resets all checkboxes to the unchecked state
    def resetAllCompletions(self):
        self.cbCAndariel.setChecked(False)
        self.cbCDuriel.setChecked(False)
        self.cbCMephisto.setChecked(False)
        self.cbCDiablo.setChecked(False)
        self.cbCBaal.setChecked(False)
        self.cbCPindleskin.setChecked(False)
        self.cbCNihlathak.setChecked(False)
        self.cbCSummoner.setChecked(False)
        self.cbCCountess.setChecked(False)
        self.cbCCouncil.setChecked(False)
        self.cbCPit.setChecked(False)
        self.cbCTunnels.setChecked(False)
        self.cbCTravincal.setChecked(False)
        self.cbCCows.setChecked(False)

    # opens a web link to the user manual
    def openManual(self):
        webbrowser.open("http://google.com")

    # used to open a backup .run file in case of a crash/error to prevent loss of user data
    def restoreRuns(self):
        run_dir = "saved/runs/"
        run_filename = QFileDialog.getOpenFileName(self, "Open File", run_dir, "Run Files (*.run)")
        run_filename = run_filename[0]
        if run_filename:
            run64_data = open(run_filename, "rb").read()
            run_data_bytes = base64.b64decode(run64_data)
            run_data_decoded = run_data_bytes.decode('ascii')

            run_dict = self.decodeJSON(run_data_decoded)
            logger.info(str("Loading run file: {}").format(run_filename))

            if run_dict:
                # Check tracker version number
                if run_dict[0]["tracker_version"] not in compatible_versions:
                    # Inform user that you cannot use a different tracker version save
                    error_box = QMessageBox()
                    error_box.setIcon(QMessageBox.Critical)
                    error_box.setWindowTitle("Version mismatch")
                    error_box.setText("Run tracker cannot load a file made from another version")
                    error_box.setStandardButtons(QMessageBox.Ok)
                    rsp = error_box.exec_()
                else:
                    # Set defaults first before applying anything because we don't want to add on to anything
                    self.setDefaults()
                    # Restore settings
                    total_runs = run_dict[-1]["total_runs"]
                    run_dict = run_dict[:-1]
                    last_item_number = len(run_dict) - 1
                    self.lineSessionName.setText(run_dict[last_item_number]["session_name"])
                    self.spinboxSessionPlayers.setValue(run_dict[last_item_number]["players"])
                    self.comboSessionDifficulty.setCurrentIndex(run_dict[last_item_number]["difficulty"])
                    self.labelSessionRunNumberCounter.setText(str(run_dict[last_item_number]["run_number"]))
                    self.setCurrentRunNumber(run_dict[last_item_number]["run_number"])
                    self.comboCharClass.setCurrentIndex(int(run_dict[last_item_number]["class"]))
                    self.spinboxCharacterLevel.setValue(run_dict[last_item_number]["level"])
                    self.spinboxCharacterMF.setValue(run_dict[last_item_number]["mf"])

                    # parse completions
                    # get the string
                    completions_string = str(run_dict[last_item_number]["completions"])
                    # iterate through looking for each character
                    if "A" in completions_string:
                        self.cbCAndariel.setChecked(True)
                    if "Du" in completions_string:
                        self.cbCDuriel.setChecked(True)
                    if "M" in completions_string:
                        self.cbCMephisto.setChecked(True)
                    if "D" in completions_string:
                        self.cbCDiablo.setChecked(True)
                    if "B" in completions_string:
                        self.cbCBaal.setChecked(True)
                    if "P" in completions_string:
                        self.cbCPindleskin.setChecked(True)
                    if "N" in completions_string:
                        self.cbCNihlathak.setChecked(True)
                    if "S" in completions_string:
                        self.cbCSummoner.setChecked(True)
                    if "C" in completions_string:
                        self.cbCCountess.setChecked(True)
                    if "mc" in completions_string:
                        self.cbCCouncil.setChecked(True)
                    if "p" in completions_string:
                        self.cbCPit.setChecked(True)
                    if "ac" in completions_string:
                        self.cbCTunnels.setChecked(True)
                    if "t" in completions_string:
                        self.cbCTravincal.setChecked(True)
                    if "c" in completions_string:
                        self.cbCCows.setChecked(True)

                    # handle run counter
                    self.setCurrentRunNumber(total_runs)
                    self.labelSessionRunNumberCounter.setText(str(total_runs))

                    # add items to list
                    for item in run_dict:
                        self.addItemToFoundList(item["tracker_version"],
                                                item["session_name"],
                                                item["run_number"],
                                                item["item_name"],
                                                item["item_type"],
                                                item["item_quantity"],
                                                item["item_ethereal"],
                                                item["completions"],
                                                item["difficulty"],
                                                item["class"],
                                                item["level"],
                                                item["mf"],
                                                item["players"],
                                                item["time_found"])

                # update the table
                self.updateItemsFoundTable()

    # opens a .json file for viewing previous sessions or to generate a report
    def openSession(self):
        session_dir = "saved/sessions/"
        session_filename = QFileDialog.getOpenFileName(self, "Open File", session_dir, "Session Files (*.json)")
        session_filename = session_filename[0]
        if session_filename:
            session_data = open(session_filename, "rb").read()
            session_dict = self.decodeJSON(session_data)

            logger.info(str("Loading session file: {}").format(session_filename))

            if session_dict:
                # Check tracker version number
                if session_dict[0]["tracker_version"] not in compatible_versions:
                    # Inform user that you cannot use a different tracker version save
                    error_box = QMessageBox()
                    error_box.setIcon(QMessageBox.Critical)
                    error_box.setWindowTitle("Version mismatch")
                    error_box.setText("Run tracker cannot load a file made from another version")
                    error_box.setStandardButtons(QMessageBox.Ok)
                    rsp = error_box.exec_()
                else:
                    # Set defaults first before applying anything because we don't want to add on to anything
                    self.setDefaults()
                    # Restore settings - subtract 2 to avoid pulling from the current_run key
                    total_runs = session_dict[-1]["total_runs"]
                    session_dict = session_dict[:-1]
                    last_item_number = len(session_dict) - 1
                    self.lineSessionName.setText(session_dict[last_item_number]["session_name"])
                    self.spinboxSessionPlayers.setValue(session_dict[last_item_number]["players"])
                    self.comboSessionDifficulty.setCurrentIndex(session_dict[last_item_number]["difficulty"])
                    self.labelSessionRunNumberCounter.setText(str(session_dict[last_item_number]["run_number"]))
                    self.setCurrentRunNumber(session_dict[last_item_number]["run_number"])
                    self.comboCharClass.setCurrentIndex(int(session_dict[last_item_number]["class"]))
                    self.spinboxCharacterLevel.setValue(session_dict[last_item_number]["level"])
                    self.spinboxCharacterMF.setValue(session_dict[last_item_number]["mf"])

                    # parse completions
                    # get the string
                    completions_string = str(session_dict[last_item_number]["completions"])
                    # iterate through looking for each character
                    if "A" in completions_string:
                        self.cbCAndariel.setChecked(True)
                    if "Du" in completions_string:
                        self.cbCDuriel.setChecked(True)
                    if "M" in completions_string:
                        self.cbCMephisto.setChecked(True)
                    if "D" in completions_string:
                        self.cbCDiablo.setChecked(True)
                    if "B" in completions_string:
                        self.cbCBaal.setChecked(True)
                    if "P" in completions_string:
                        self.cbCPindleskin.setChecked(True)
                    if "N" in completions_string:
                        self.cbCNihlathak.setChecked(True)
                    if "S" in completions_string:
                        self.cbCSummoner.setChecked(True)
                    if "C" in completions_string:
                        self.cbCCountess.setChecked(True)
                    if "mc" in completions_string:
                        self.cbCCouncil.setChecked(True)
                    if "p" in completions_string:
                        self.cbCPit.setChecked(True)
                    if "ac" in completions_string:
                        self.cbCTunnels.setChecked(True)
                    if "t" in completions_string:
                        self.cbCTravincal.setChecked(True)
                    if "c" in completions_string:
                        self.cbCCows.setChecked(True)

                    # handle run counter
                    self.setCurrentRunNumber(total_runs)
                    self.labelSessionRunNumberCounter.setText(str(total_runs))

                    # add items to list
                    for item in session_dict:
                        self.addItemToFoundList(item["tracker_version"],
                                                item["session_name"],
                                                item["run_number"],
                                                item["item_name"],
                                                item["item_type"],
                                                item["item_quantity"],
                                                item["item_ethereal"],
                                                item["completions"],
                                                item["difficulty"],
                                                item["class"],
                                                item["level"],
                                                item["mf"],
                                                item["players"],
                                                item["time_found"])

                # update the table
                self.updateItemsFoundTable()

    # generates a text file containing a rudimentary report
    def generateReport(self):
        difficulty_list = ["Normal", "Nightmare", "Hell"]
        class_list = ["Amazon", "Assassin", "Barbarian", "Druid", "Necromancer", "Paladin", "Sorceress"]
        report_item_list = deepcopy(self.getFoundItemList())

        total_items = len(report_item_list)
        if total_items <= 0:
            # Inform user there is nothing to generate
            error_box = QMessageBox()
            error_box.setIcon(QMessageBox.Critical)
            error_box.setWindowTitle("Cannot Generate Report")
            error_box.setText("Found item list is empty - report cannot be generated")
            error_box.setStandardButtons(QMessageBox.Ok)
            rsp = error_box.exec_()
            return
        else:
            if "total_runs" in report_item_list[-1]:
                report_item_list = report_item_list[:-1]
            for item in report_item_list:
                item.pop("tracker_version")
                item["difficulty"] = difficulty_list[item["difficulty"]]
                item["class"] = class_list[item["class"]]
                if item["item_ethereal"]:
                    item["item_ethereal"] = "Eth"
                else:
                    item["item_ethereal"] = ""


            table = PrettyTable(["Session Name", "Run #", "Item Name", "Type", "Quant", "Eth", "Completions",
                                 "Difficulty", "Class", "Level", "MF", "Players", "Time Found"])
            for item in report_item_list:
                item_as_list = list(dict(item).values())
                table.add_row(item_as_list)

            total_runs = self.getCurrentRunNumber()

            reports_path = Path("reports")
            if not reports_path.exists():
                Path(reports_path).mkdir(parents=True, exist_ok=True)
            o = open(str(reports_path) + "/" + self.getSessionName() + ".txt", "w")
            o.write(str(table))
            final_tally = "\nTotal items found: " + str(total_items) + "\nTotal runs completed: " + str(total_runs)
            o.write(final_tally)
            o.close()

    def displayAboutWindow(self):
        # Display program about info
        about_box = QMessageBox()
        about_box.setIcon(QMessageBox.NoIcon)
        about_box.setWindowTitle("Diablo 2 Run Tracker")
        about_box.setText(str("Diablo 2 Run Tracker\n\nAuthor: Rob Durst\n\nVersion: {0}").format(__version__))
        about_box.setStandardButtons(QMessageBox.Close)
        rsp = about_box.exec_()

    # called to close the program
    def exitApp(self):
        QtWidgets.qApp.quit()

def my_handler(type, value, tb):
    logger.exception("Uncaught exception: {0}".format(str(value)))

def begin_log_file():
    logger.info("OS Name: " + os.name)
    logger.info("Python version: " + sys.version)
    logger.info("D2 Run Tracker Version: " + __version__)

if __name__ == "__main__":
    import sys
    sys.excepthook = my_handler
    begin_log_file()
    app = QtWidgets.QApplication(sys.argv)
    window = d2runtracker()
    window.show()
    sys.exit(app.exec_())
