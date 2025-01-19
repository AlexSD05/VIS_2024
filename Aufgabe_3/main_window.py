from __future__ import annotations

from PySide6.QtCore import Slot
from PySide6.QtGui import QAction, QKeySequence, QScreen
from PySide6.QtWidgets import QMainWindow, QFileDialog


from main_widget import widget
from mbsModel import mbsModel


class MainWindow(QMainWindow):
    def __init__(self, ):
        QMainWindow.__init__(self)
        self.setWindowTitle("FDD File Reader")

        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")

        # Menu Sonstiges
        self.HelpMenu = self.menu.addMenu("Sonstiges")

        # Help Action
        help_action = QAction("Help", self)
        self.HelpMenu.addAction(help_action)
        self.HelpMenu.triggered.connect(self.helpaction)

        #Load QAction
        load_action = QAction("Load", self)

        load_action.triggered.connect(self.loadfile)

        self.file_menu.addAction(load_action)

        #Save QAction
        save_action = QAction("Save", self)

        save_action.triggered.connect(self.savemodel)

        self.file_menu.addAction(save_action)


        #ImportFDD QAction
        import_action = QAction("ImportFDD", self)

        import_action.triggered.connect(self.importfile)

        self.file_menu.addAction(import_action)

        # Exit QAction
        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)

        self.file_menu.addAction(exit_action)

        # Status Bar
        self.status = self.statusBar()
        self.status.showMessage("Error 404: Brain not found", 3000)

        # Window dimensions
        geometry = self.screen().availableGeometry()
        self.setFixedSize(geometry.width() * 0.8, geometry.height() * 0.7)

        self.widget = widget(self)
        self.setCentralWidget(self.widget)

    def loadfile(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "load File", "", "pyFreeDyn-File (*.json)")
        self.mbsModel = mbsModel()
        self.mbsModel.loadDatabase(filePath)
        self.widget.rendererMbsModel(self.mbsModel)
        self.status.showMessage("File loaded. Let's Go",3000)

    def importfile(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "import File", "", "pyFreeDyn-File (*.fdd)")
        self.mbsModel = mbsModel()
        self.mbsModel.importFddFile(filePath)
        self.widget.rendererMbsModel(self.mbsModel)
        self.status.showMessage("File imported",3000)

    def savemodel(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "save File", "", "pyFreeDyn-File (*.json)")
        self.mbsModel.saveDatabase(filePath)
        self.status.showMessage("File saved",3000)

    def helpaction(self):
        self.status.showMessage("Mir ist nicht mehr zu helfen",3000)