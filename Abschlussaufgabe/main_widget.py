from __future__ import annotations

from PySide6.QtCore import QDateTime, Qt
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import (QWidget, QHeaderView, QHBoxLayout, QTableView,
                               QSizePolicy)
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QDateTimeAxis, QValueAxis
#-----------------------------------------------------------------------------------
import sys
from pathlib import Path

from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer
)
from vtkmodules.all import vtkInteractorStyleTrackballCamera

import QVTKRenderWindowInteractor as QVTK
import vtk
from vtkmodules.vtkCommonDataModel import vtkBoundingBox



class widget(QWidget):
#class Widget(QVTK.QVTKRenderWindowInteractor):
    def __init__(self, data):
        QWidget.__init__(self)

        self.layout = QHBoxLayout()

    def rendererMbsModel(self, mbsModel):
        self.qvtkWidget = QVTK.QVTKRenderWindowInteractor(self)  #Schnittstelle vtk und Widget
        self.layout.addWidget(self.qvtkWidget)
        self.setLayout(self.layout)

        #visualization part
        #-----------------------------------------------------------------------------
        self.renderer = vtkRenderer()
        self.renderWindow = self.qvtkWidget.GetRenderWindow()    #Renderer Hinzufügen
        self.renderWindow.AddRenderer(self.renderer)


        # Interactor einrichten
        interactor = self.qvtkWidget.GetRenderWindow().GetInteractor()
        interactor.SetRenderWindow(self.renderWindow)

        style = vtkInteractorStyleTrackballCamera()
        interactor.SetInteractorStyle(style)

        # Modell anzeigen
        mbsModel.showModel(self.renderer)


        # Render- und Interaktionsloop starten
        self.renderWindow.Render()
        interactor.Start()

