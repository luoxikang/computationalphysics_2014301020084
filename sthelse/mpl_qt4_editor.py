# -*- coding: utf-8 -*-
"""
Created on Sun Feb 14 21:03:37 2016

@author: Administrator
"""

import sys
from PyQt4 import QtGui
from traitsui.qt4.editor import Editor
from traitsui.basic_editor_factory import BasicEditorFactory
import matplotlib
matplotlib.use("QT4Agg")
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar



class _MPLFigureEditor(Editor):
    scrollable = True
    
    def init(self,parent):
        self.control = self._create_canvas()
        self.set_tooltip()
    
    def update_editor(self):
        pass
    
    def _create_canvas(self):
        m_widget = QtGui.QWidget()
        vbl = QtGui.QVBoxLayout(m_widget)
        qmc = Qt4MplCanvas(m_widget, self.value)
        ntb = NavigationToolbar(qmc, m_widget)
        vbl.addWidget(qmc)
        vbl.addWidget(ntb)
        return m_widget

class MPLFigureEditor(BasicEditorFactory):
    klass = _MPLFigureEditor
    

class Qt4MplCanvas(FigureCanvas):
    def __init__(self, parent,fig):
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        
#class ApplicationWindow(QtGui.QMainWindow):
#    def __init__(self):
#        QtGui.QMainWindow.__init__(self)
#        self.setWindowTitle("Matplotlib Figure in QT4")
#        self.main_widget=QtGui.QWidget(self)
#        vbl = QtGui.QVBoxLayout(self.main_widget)
#        qmc = Qt4MplCanvas(self.main_widget)
#        ntb = NavigationToolbar(qmc, self.main_widget)
#        vbl.addWidget(qmc)
#        vbl.addWidget(ntb)
#        
#        self.main_widget.setFocus()
#        self.setCentralWidget(self.main_widget)
#        
#qApp = QtGui.QApplication(sys.argv)
#aw = ApplicationWindow()
#aw.show()
#sys.exit(qApp.exec_())

if __name__ == "__main__":
    from matplotlib.figure import Figure
    from traits.api import HasTraits, Instance
    from traitsui.api import View, Item
    from numpy import sin, linspace , pi
    
    class Test(HasTraits):
        figure = Instance(Figure, ())
        view = View(
        Item('figure', editor=MPLFigureEditor(), show_label=False),
        width = 400,
        height = 300,
        resizable = True)
        
        def __init__(self):
            super(Test, self).__init__()
            axes = self.figure.add_subplot(111)
            t = linspace(0, 2*pi, 200)
            axes.plot(sin(t))
            
    Test().configure_traits()
        