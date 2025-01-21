from __future__ import annotations

from PySide6.QtCore import Slot, Qt
from PySide6.QtGui import QAction, QKeySequence, QScreen, QColor
from PySide6.QtWidgets import QMainWindow, QFileDialog, QColorDialog, QDialog, QPushButton, QVBoxLayout, QGroupBox, QLabel, QSlider, QHBoxLayout, QLineEdit


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

        # Menu Settings
        self.SettingsMenu = self.menu.addMenu("Settings")

        # Body Color
        self.bodycolor_action = QAction("Bodycolor", self)
        self.SettingsMenu.addAction(self.bodycolor_action)
        self.bodycolor_action.triggered.connect(lambda: self.bodycoloraction())

        # Background Settings
        self.background_action = QAction("Background", self)
        self.SettingsMenu.addAction(self.background_action)
        self.background_action.triggered.connect(lambda: self.backgroundaction())

        # Help Action
        self.help_action = QAction("Help", self)
        self.HelpMenu.addAction(self.help_action)
        self.help_action.triggered.connect(self.helpaction)

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

#Ändern der Hintergrundfarbe
#----------------------------------------------------------------------------------------------------------------------------
    def backgroundaction(self):
        backgroundcolor = QColorDialog.getColor()   #Öffnet Farbpalette
        
        # Abfrage, ob gültiger rgb wert eingegeben wurde
        if backgroundcolor.isValid():
            self.backgroundcolorRGB = backgroundcolor.red(), backgroundcolor.green(), backgroundcolor.blue()
        
        self.mbsModel.backgroundcolor = self.backgroundcolorRGB
        self.widget.renderer.SetBackground([element / 255 for element in self.mbsModel.backgroundcolor])    #Skalierung durch 255, um auf den Bereich zu bringen

# Ändern der Körper Farben und Transparenz
# Hinzufügen von Parametern für die json datei
# transparecy und name
#----------------------------------------------------------------------------------------------------------------------------
    def bodycoloraction(self):

        bodycolorwindow = QDialog()
        bodycolorwindow.setWindowTitle("Bodycolor Settings")    # Name des Fensters
        mainlayout = QVBoxLayout(bodycolorwindow)   # Layout

        # Manuelle Fenstergröße festlegen
        #geometry = bodycolorwindow.screen().availableGeometry()
        #bodycolorwindow.setFixedSize(geometry.width() * 0.5, geometry.height() * 0.4)
        
        self.listofbodies = []  # Erstellen einer leeren liste, um alle Körper einzubinden

        # Einfügen aller Körper in listofbodies
        for obj in self.mbsModel.getlistofmbyObject():
            if obj.getType() == "Body":
                self.listofbodies.append(obj)
        
        self.anzeigefarbe = []

        # Durchlaufen aller BOdies
        for body in self.listofbodies:
            unterwindow = QGroupBox(f"properties {body.parameter["name"]["value"]}")  # f davor: Geschwungene klammer ein element, was nicht ein String ist
            layout = QVBoxLayout(unterwindow)   # Auswählen des Layouts
            mainlayout.addWidget(unterwindow)   # Fenster In Fenster einbinden

            labelcolor = QLabel("Color")
            layout.addWidget(labelcolor)        # Hinzufügen Label Color

            # kleiner Kasten zum Anzeigen der ausgewählten Farbe
            self.anzeigefarbe.append(QLineEdit())
            self.anzeigefarbe[self.listofbodies.index(body)].setReadOnly(True)

            # Anzeigen der ausgewählten Farbe
            colorshow = QColor(body.parameter["color"]["value"][0], body.parameter["color"]["value"][1], body.parameter["color"]["value"][2])
            self.anzeigefarbe[self.listofbodies.index(body)].setStyleSheet(f"background-color: {colorshow.name()};")       
            layout.addWidget(self.anzeigefarbe[self.listofbodies.index(body, self.listofbodies.index(body))])

            #Knopf zum Auswählen der Farbe
            buttoncolor = QPushButton("Choose Color")
            buttoncolor.clicked.connect(lambda checked, bodycolor = body, index = self.listofbodies.index(body): self.bodycolor(bodycolor, index))
            layout.addWidget(buttoncolor)       # Hinzufügen von Color Button

            # Transparenz der Körper einstellen
            #----------------------------------------------------------------------------------------------------------------------------
            labeltransparency = QLabel("Transparency")  # Beschriftung des Sliders
            layout.addWidget(labeltransparency)

            layoutslider = QHBoxLayout()
            labelsliderleft = QLabel("0 %")     # BEschriftung SLider Links
            layoutslider.addWidget(labelsliderleft)     # Beschriftung Links hinzufügen
            
            slidertransparency = QSlider(Qt.Horizontal)     # SLider Horizontal
            slidertransparency.setMinimum(0)        # Minimumwert festlegen
            slidertransparency.setMaximum(100)      # Maximumwert festlegen

            # /255*100 weil transparenz von 0 - 255 im Ursprungsfile geht
            slidertransparency.setValue(body.parameter["transparency"]["value"]/255*100)    

            # Slider Updaten bei Änderung der Stellung
            slidertransparency.valueChanged.connect(lambda value, bodyslider = body: self.updatetransparency(value, bodyslider))

            layoutslider.addWidget(slidertransparency)
            labelsliderright = QLabel("100 %")      # Beschriftung rechts
            layoutslider.addWidget(labelsliderright)    # Hinzufügen Beschriftung Rechts

            layout.addLayout(layoutslider)      # Slider zu Layout hinzufügen

        

        okbutton = QPushButton("Okidoki")       # Anlegen des OKaybuttons
        okbutton.clicked.connect(lambda: self.clickok(bodycolorwindow))     # Festlegen was bei klicken passiert
        mainlayout.addWidget(okbutton)      # Button hinzufügen zu layout

        bodycolorwindow.exec()      # Fenster ausführen

    # Funktion zum Updaten der Transparenz
    def updatetransparency(self, value, body):
        body.parameter["transparency"]["value"] = value *255/100    # Transparenz geht von 0 bis 255 soll aber von 0 bis 100 sein

    # Funktion zum Festlegen einer Farbe
    def bodycolor(self, body, indexbody):
        bodycolor = QColorDialog.getColor()   #Öffnet Farbpalette        
        if bodycolor.isValid():
            body.parameter["color"]["value"] = bodycolor.red(), bodycolor.green(), bodycolor.blue()
            self.anzeigefarbe[indexbody].setStyleSheet(f"background-color: {bodycolor.name()};")
        
        #self.mbsModel.bodycolor = self.backgroundcolorRGB
        #self.widget.renderer.SetBackground([element / 255 for element in self.mbsModel.backgroundcolor])

    # Funktion beim klicken des okay buttons
    # Aktualisert Modelle
    def clickok(self, window):
        for body in self.listofbodies:
            body.hide(self.widget.renderer)
            body.updateactor()  # Aufrufender upadteactor FUnktion in body.py
            body.show(self.widget.renderer)


        window.accept()