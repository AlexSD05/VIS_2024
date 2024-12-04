
#Chapter 1
#--------------------------------------------------------------------------------------------------
# from __future__ import annotations

# import argparse
# import pandas as pd


# def read_data(fname):
#     return pd.read_csv(fname)


# if __name__ == "__main__":
#     options = argparse.ArgumentParser()
#     options.add_argument("-f", "--file", type=str, required=True)
#     args = options.parse_args()
#     data = read_data(args.file)
#     print(data)
    
#Chapter 2
#-------------------------------------------------------------------------------------------------

from __future__ import annotations


import argparse

import pandas as pd


from PySide6.QtCore import QDateTime, QTimeZone



def transform_date(utc, timezone=None):

    utc_fmt = "yyyy-MM-ddTHH:mm:ss.zzzZ"

    new_date = QDateTime().fromString(utc, utc_fmt)

    if timezone:

        new_date.setTimeZone(timezone)

    return new_date



def read_data(fname):

    # Read the CSV content

    df = pd.read_csv(fname)


    # Remove wrong magnitudes

    df = df.drop(df[df.mag < 0].index)

    magnitudes = df["mag"]


    # My local timezone

    timezone = QTimeZone(b"Europe/Berlin")


    # Get timestamp transformed to our timezone

    times = df["time"].apply(lambda x: transform_date(x, timezone))


    return times, magnitudes



if __name__ == "__main__":

    options = argparse.ArgumentParser()

    options.add_argument("-f", "--file", type=str, required=True)

    args = options.parse_args()

    data = read_data(args.file)

    print(data)

#Chapter 3
#------------------------------------------------------------------------------------------------

from PySide6.QtCore import Slot
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Eartquakes information")

        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")

        # Exit QAction
        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)

        self.file_menu.addAction(exit_action)

        # Status Bar
        self.status = self.statusBar()
        self.status.showMessage("Data loaded and plotted")

        # Window dimensions
        geometry = self.screen().availableGeometry()
        self.setFixedSize(geometry.width() * 0.8, geometry.height() * 0.7)