from __future__ import print_function

###### PyQt import line ######
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
###### PyQt import line ######

import webbrowser
from gTask_importer_pre_release import *

import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pandas as pd
from tqdm import tqdm
import time

form_class = uic.loadUiType("gtask_to_csv.ui")[0]
credential = None 

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        ## Connect btn event 
        self.pushButton.clicked.connect(self.btn1_clicked)
        self.pushButton_2.clicked.connect(self.btn2_clicked)
        self.pushButton_3.clicked.connect(self.btn3_clicked)
        self.pushButton_4.clicked.connect(self.btn4_clicked)

    # Enable Google API via External URL
    def btn1_clicked(self):
        webbrowser.open_new_tab("https://developers.google.com/tasks/quickstart/python")
        self.textEdit.append("1. Enable Google API via External URL")

    # Login with Google OAuth
    def btn2_clicked(self):
        google_authentication()
        self.textEdit.append("2. Login with Google OAuth")
        QMessageBox.about(self, "message", "Step 3 would be take more than 10 minutes depends on your tasks size")


    # Get CSV file from Google Task
    def btn3_clicked(self):
        self.textEdit.append("3. Get CSV file from Google Task")
        QMessageBox.about(self, "message", "Please see the enclosing folder")
        get_csv_from_tasks()
        self.textEdit.append("Done!")
        self.textEdit.append("====================================================")

        text_message = """ 
        Developer: Yunho Maeng
        Version: v0.3
        Release Date: 2019-10-08

        Please check out Github repository for up-to-date version
        https://github.com/yunho0130/gTask_to_CSV
        """
        self.textEdit.append(text_message)

    # Check the updated version 
    def btn4_clicked(self):
        webbrowser.open_new_tab("https://github.com/yunho0130/gTask_to_CSV")
    # # Open credentails.json file
    # def btn4_clicked(self):
    #     fname = QFileDialog.getOpenFileName(self)
    #     credential = QtCore.QFile(fname[0])

# import logging

# class QPlainTextEditLogger(logging.Handler):
#     def __init__(self, parent):
#         super(Logger, self).__init__()
#         self.widget = QPlainTextEdit(parent)
#         self.widget.setReadOnly(True)

#     def emit(self, record):
#         msg = self.format(record)
#         self.widget.textCursor().appendPlainText(msg)

#     def write(self, m):
#         pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()