from __future__ import annotations

from PySide6.QtCore import Slot
from PySide6.QtGui import QAction, QKeySequence, QScreen
from PySide6.QtWidgets import QMainWindow


class MainWindow(QMainWindow):
    def __init__(self, widget):
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

        # Test Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("TestMenu")

        #Test QAction
        test_action = QAction("Test", self)

        self.file_menu.addAction(test_action)

        # Status Bar
        self.status = self.statusBar()
        self.status.showMessage("Data loaded and plotted")

        # Window dimensions
        geometry = self.screen().availableGeometry()
        self.setFixedSize(geometry.width() * 0.8, geometry.height() * 0.7)
        self.setCentralWidget(widget)