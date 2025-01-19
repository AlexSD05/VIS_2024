import mbsModel
import sys
from pathlib import Path

from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer
)
from vtkmodules.all import vtkInteractorStyleTrackballCamera

#QT Window Application
from PySide6.QtWidgets import QApplication
from main_window import MainWindow


#-----------------------------------------------------------------------------
# Qt Application
app = QApplication(sys.argv)

window = MainWindow()

window.show()
sys.exit(app.exec())