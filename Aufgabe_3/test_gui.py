import sys
from PySide6.QtWidgets import QMainWindow, QApplication
from vtkmodules.vtkRenderingCore import vtkRenderer
from vtkmodules.all import vtkConeSource, vtkPolyDataMapper, vtkActor
import QVTKRenderWindowInteractor as QVTK
QVTKRenderWindowInteractor = QVTK.QVTKRenderWindowInteractor

def QVTKRenderWidgetConeExample(argv):
    app = QApplication(['QVTKRenderWindowInteractor'])
    window = QMainWindow()
    widget = QVTKRenderWindowInteractor(window)
    window.setCentralWidget(widget)
    ren = vtkRenderer()
    widget.GetRenderWindow().AddRenderer(ren)
    cone = vtkConeSource()
    cone.SetResolution(8)
    coneMapper = vtkPolyDataMapper()
    coneMapper.SetInputConnection(cone.GetOutputPort())
    coneActor = vtkActor()
    coneActor.SetMapper(coneMapper)
    ren.AddActor(coneActor)
    window.show()
    widget.Initialize()
    widget.Start()
    app.exec()

if __name__ == "__main__":
    QVTKRenderWidgetConeExample(sys.argv)