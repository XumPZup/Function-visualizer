import re
import sys
from PyQt5.QtWidgets import (QMainWindow, QWidget, QApplication, QGridLayout,
                             QPushButton, QGroupBox, QLineEdit, QLabel, QGroupBox,
                             QVBoxLayout, QDoubleSpinBox, QCheckBox, QButtonGroup)
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, Qt
from PyQt5.QtGui import QDoubleValidator, QIntValidator
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import time
import numpy as np
from numpy import (pi, e, sin, cos, tan, arcsin, arccos, arctan,
                   sqrt, power, floor, ceil)




class ThreadSignals(QThread):
    signal = pyqtSignal(str)

    def __init__(self):
        QThread.__init__(self)
        self.running = False
        self.steps = np.zeros(0)
        self.last = 0
        self.varInput = None
        self.xFunction = None
        self.yFunction = None
        
    def run(self):
        while self.running:
            time.sleep(1)
            self.varInput.setText(str(np.round(self.steps[self.last],3)))
            self.last += 1
            self.signal.emit('')
            if self.last > len(self.steps) - 1:
                self.running = False
                self.last = 0
            


       
class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.window = QWidget(self)
        self.grid = QGridLayout()
        self.window.setLayout(self.grid)
        self.title = 'Unit Circle Test'
        self.left = 100
        self.top = 40
        self.width = 1000
        self.height = 970
        self.accuracy = 100
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setCentralWidget(self.window)
        # - Graph frames
        self.xyGraph = MplCanvas('XY' ,None, width=6, height=6)
        self.xGraph = MplCanvas('X' ,None, width=6, height=6)
        self.yGraph = MplCanvas('Y' ,None, width=6, height=6)
    
        # - Graph buttons Box # ---------------------------------
        self.plotButtonsBox = QGroupBox('Plot/Clear')
            # - Plot Function Btn
        self.plotFunctionBtn = QPushButton('Plot Function')
        self.plotFunctionBtn.clicked.connect(self.plot_function)
            # - Clear Plot Bnt
        self.clearPlotBtn = QPushButton('Clear Plot')
        self.clearPlotBtn.clicked.connect(self.clear_plots)
            # - Layout
        self.plotButtonsLayout = QVBoxLayout()
        self.plotButtonsLayout.addWidget(self.plotFunctionBtn)
        self.plotButtonsLayout.addWidget(self.clearPlotBtn)
        # -
        self.plotButtonsBox.setLayout(self.plotButtonsLayout)
        self.plotButtonsBox.setMaximumWidth(110)
        self.plotButtonsBox.setMinimumWidth(110)
        self.plotButtonsBox.setMaximumHeight(140)
        # -------------------------------------------------------
        # -------------------------------------------------------
        # - X & Y function Box - # ------------------------------
        self.functionBox = QGroupBox('Function')
            # - X Label&Input
        self.xLabel = QLabel('X:')
        self.xInput = QLineEdit()
#        self.xInput.setFixedWidth(300)
            # - y Label&Input
        self.yLabel = QLabel('Y:')
        self.yInput = QLineEdit()
            # - Legend Checkbox
        self.plotLegend = QCheckBox('Legend')
            # - Layout
        self.functionLayout = QGridLayout()
        self.functionLayout.addWidget(self.xLabel, 0, 0)
        self.functionLayout.addWidget(self.xInput, 0, 1)
        self.functionLayout.addWidget(self.yLabel, 1, 0)
        self.functionLayout.addWidget(self.yInput, 1, 1)
        self.functionLayout.addWidget(self.plotLegend, 2, 0, 1, 2)
        # -
        self.functionBox.setLayout(self.functionLayout)
        self.functionBox.setMaximumWidth(350)
        self.functionBox.setMinimumWidth(350)
        self.functionBox.setMaximumHeight(140)
        # --------------------------------------------------------
        # --------------------------------------------------------
        # - Variables Info Box - # ------------------------------------
        self.variablesInfoBox = QGroupBox('Function')
            # - Labes
        self.thetaLabel = QLabel('0 < u < 2*pi')
        self.theta2Label = QLabel('0 < t < 2*pi')
        self.xFunctionLabel = QLabel('X = None')
        self.yFunctionLabel = QLabel('Y = None')
        self.accuracyLabel = QLabel('Accuracy = ' + str(self.accuracy))
            # - Layout
        self.variablesInfoLayout = QGridLayout()
        self.variablesInfoLayout.addWidget(self.thetaLabel, 0, 0)
        self.variablesInfoLayout.addWidget(self.theta2Label, 0, 1)
        self.variablesInfoLayout.addWidget(self.accuracyLabel, 0, 2)
        # --
        self.variablesInfoLayout.addWidget(self.xFunctionLabel, 1, 0, 1, 3)
        self.variablesInfoLayout.addWidget(self.yFunctionLabel, 2, 0, 1, 3)
        # - 
        self.variablesInfoBox.setLayout(self.variablesInfoLayout)
        self.variablesInfoBox.setMaximumWidth(350)
        self.variablesInfoBox.setMinimumWidth(350)
        self.variablesInfoBox.setMaximumHeight(140)
        # -------------------------------------------------------------
        # -------------------------------------------------------------
        # - Variable Increment Box ------------------------------------
        self.variableIncrementBox = QGroupBox('Gradual Increment')
            # - Labels&Inputs
        self.variableLabel = QLabel('Var:')
        self.variableInput = QLineEdit()
        self.startLabel = QLabel('Start:')
        self.startInput = QLineEdit()
        self.startInput.setValidator(QDoubleValidator(-100,100,3))
        self.stopLabel = QLabel('Stop:')
        self.stopInput = QLineEdit()
        self.stopInput.setValidator(QDoubleValidator(-100,100,3))
        self.stepLabel = QLabel('Step:')
        self.stepInput = QLineEdit()
        self.stepInput.setValidator(QDoubleValidator(-100,100,3))
            # - Toggle Incremente Button
        self.toggleIncrementBtn = QPushButton('Toggle Increment')
        self.toggleIncrementBtn.clicked.connect(self.toggle_increment)
            # - Checobox
        self.autoClearPlot = QCheckBox('Clear')
            # - Layout
        self.variableIncrementLayout = QGridLayout()
        self.variableIncrementLayout.addWidget(self.startLabel, 0, 0)
        self.variableIncrementLayout.addWidget(self.startInput, 0, 1)
        self.variableIncrementLayout.addWidget(self.stopLabel, 0, 2)
        self.variableIncrementLayout.addWidget(self.stopInput, 0, 3)
        # -
        self.variableIncrementLayout.addWidget(self.stepLabel, 1, 0)
        self.variableIncrementLayout.addWidget(self.stepInput, 1, 1)
        self.variableIncrementLayout.addWidget(self.variableLabel, 1, 2)
        self.variableIncrementLayout.addWidget(self.variableInput, 1, 3)
        # -
        self.variableIncrementLayout.addWidget(self.toggleIncrementBtn, 2, 0, 1, 3)
        self.variableIncrementLayout.addWidget(self.autoClearPlot, 2, 3)
        # --
        self.variableIncrementBox.setLayout(self.variableIncrementLayout)
        self.variableIncrementBox.setMinimumWidth(220)
        self.variableIncrementBox.setMaximumWidth(220)
        self.variableIncrementBox.setMaximumHeight(140)
        # -------------------------------------------------------------
        # -------------------------------------------------------------
        # - Additional Variables Box - # ------------------------------
        self.variablesBox = QGroupBox('Additional Variables')
        self.varNames = ['accuracy', 'a', 'b', 'm','n1', 'n2', 'n3',
                         'n4', 'n5', 'n6', 'n7', 'n8', 'n9',]
        self.anglesVar = ['u', 't']
            # - Layout
        self.variablesLayout = QGridLayout()
        self.varInputList = []
            # - Variables Label/Input
        for i in range(len(self.varNames)):
            label = QLabel(self.varNames[i] + ':')
            inp = QLineEdit()
            inp.setValidator(QDoubleValidator(-100,100,3))
            self.varInputList.append(inp)
            self.variablesLayout.addWidget(label, i, 0)
            self.variablesLayout.addWidget(inp, i, 1, 1, 2)
            if i > 0:
                inp.setText('0')
            else:
                inp.setText('100')

        self.anglesInputList = []
        for i in range(len(self.anglesVar)):
            label = QLabel('< ' + self.anglesVar[i] + ' <')
            minor = QLineEdit()
            major = QLineEdit()
            minor.setText('0')
            major.setText('2*pi')
            self.anglesInputList.append([minor, major])
            self.variablesLayout.addWidget(minor, i+len(self.varNames), 0)
            self.variablesLayout.addWidget(label, i+len(self.varNames), 1)
            self.variablesLayout.addWidget(major, i+len(self.varNames), 2)
            
        # -
        self.variablesBox.setLayout(self.variablesLayout)
        self.variablesBox.setMinimumWidth(200)
        self.variablesBox.setMaximumWidth(200)
        self.variablesBox.setMinimumHeight(140)        
        # ---------------------------------------------------------
        # ---------------------------------------------------------
        # - Change Plot Buttons -----------------------------------
        self.changePlotBox = QGroupBox('Select Plot')
        self.xyPlotBtn = QPushButton('XY')
        self.xPlotBtn = QPushButton('X')
        self.yPlotBtn = QPushButton('Y')
            # - Grouping The buttons - #
        self.btnGroup = QButtonGroup()
        self.btnGroup.addButton(self.xyPlotBtn)
        self.btnGroup.addButton(self.xPlotBtn)
        self.btnGroup.addButton(self.yPlotBtn)
        self.btnGroup.buttonClicked.connect(self.change_plot)
            # - Layout - #
        self.changePlotLayout = QGridLayout()
        self.changePlotLayout.addWidget(self.xyPlotBtn, 0, 0)
        self.changePlotLayout.addWidget(self.xPlotBtn, 0, 1)
        self.changePlotLayout.addWidget(self.yPlotBtn, 0, 2)
        self.changePlotBox.setLayout(self.changePlotLayout)
        self.changePlotBox.setMinimumWidth(200)
        self.changePlotBox.setMaximumWidth(200)
        self.changePlotBox.setMaximumHeight(70)
        # ---------------------------------------------------------
        #____________
        # - Grid
        #____________
        # --------------------------------------------- #
        self.grid.setHorizontalSpacing(0)
        self.grid.addWidget(self.plotButtonsBox, 0, 0)
        self.grid.addWidget(self.functionBox, 0, 1)
        self.grid.addWidget(self.variablesInfoBox, 0, 2)
        self.grid.addWidget(self.variableIncrementBox, 0, 3)
        # ----------------------------------------------- #
        self.grid.addWidget(self.variablesBox, 1, 3, 2, 1)
        self.grid.addWidget(self.xyGraph, 1, 0, 3, 3)
        self.grid.addWidget(self.xGraph, 1, 0, 3, 3)
        self.grid.addWidget(self.yGraph, 1, 0, 3, 3)
        # --------------------------------------------- #
        self.grid.addWidget(self.changePlotBox, 3, 3)
        # ----------------------------------------------- #
        # ----------------------------------------------------
        # ----------------------------------------------------
        self.xGraph.hide()
        self.yGraph.hide()
        self.thread = ThreadSignals()
        self.thread.signal.connect(self.plot_function)
        self.show()
        # ---------------------------------------------------------


    # --------------------------------------
    def clear_plots(self):
        self.xGraph.clear_plot()
        self.yGraph.clear_plot()
        self.xyGraph.clear_plot()


    # ---------------------------------------
    def plot_function(self):
        try:
            # - Exctracting variable values from text inputs
            accuracy, a, b, m, n1, n2, n3, n4, n5, n6, n7, n8, n9 = [float(i.text()) if i.text() != '' else None for i in self.varInputList]
            u_range, t_range = [[i[0].text(), i[1].text()] if not '' in [i[0].text(), i[1].text()] else [None, None] for i in self.anglesInputList]
            if accuracy:
                self.accuracy = int(accuracy)
            
            if not None in u_range:        
                u = np.linspace(eval(u_range[0]), eval(u_range[1]), self.accuracy)
                self.thetaLabel.setText('%s < u < %s'%(u_range[0], u_range[1]))

            if not None in t_range:        
                t = np.linspace(eval(t_range[0]), eval(t_range[1]), self.accuracy)
                self.theta2Label.setText('%s < t < %s'%(t_range[0], t_range[1]))
            
            # - Evaluating string functions
            xString = self.xInput.text()
            yString = self.yInput.text()
            x = eval(xString)
            y = eval(yString)
            # - Showing function
            self.xFunctionLabel.setText('X = ' + xString)
            self.yFunctionLabel.setText('Y = ' + yString)
            # - Show legend
            if self.plotLegend.isChecked():
                self.accuracyLabel.setText('Accuracy = ' + str(self.accuracy))
                legend = 'X = ' + xString + '\nY = ' + yString
                xLegend = legend.split('\n')[0]
                yLegend = legend.split('\n')[1]
            else:
                legend = None
                xLegend = None
                yLegend = None
            # - Auto clear plot
            if self.autoClearPlot.isChecked():
                self.xyGraph.clear_plot()
                self.xGraph.clear_plot()
                self.yGraph.clear_plot()
            # - Plotting
            self.xyGraph.plot([x, y], legend)
            self.xGraph.plot([u, x], xLegend)
            self.yGraph.plot([u, y], yLegend)
        except:
            print('Typing Error In Function')


    # -----------------------        
    def toggle_increment(self):
        try:
            if self.thread.running:
                self.thread.running = False
            else:
                start = float(self.startInput.text())
                stop = float(self.stopInput.text())
                step = float(self.stepInput.text())
                new_steps = np.arange(start, stop, step)
                inputIndex = self.varNames.index(self.variableInput.text())
                inp = self.varInputList[inputIndex]
                if self.thread.varInput != inp or not np.array_equal(new_steps, self.thread.steps):
                    self.thread.varInput = inp
                    self.thread.steps = new_steps

                self.thread.running = True
                self.thread.start()
        except:
            print('Typing Error in Gradual Increment')


    # -------------------------
    def change_plot(self, btn):
        if btn.text() == 'XY':
            self.xGraph.hide()
            self.yGraph.hide()
            self.xyGraph.show()
        elif btn.text() == 'X':
            self.xGraph.show()
            self.yGraph.hide()
            self.xyGraph.show()
        else:
            self.xGraph.hide()
            self.yGraph.show()
            self.xyGraph.hide()

        
#______________
# CANVAS PLT
#______________
class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, name, parent=None, width=5, height=5, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = self.fig.add_subplot(111)
        self.name = name
               
        FigureCanvasQTAgg.__init__(self, self.fig)
        self.setParent(parent)
        self.axLimit = 1.1
        self.legends = []
        self.clear_plot()
    # ----------------------------------------------------------

    
    def plot(self, x_y, legend=None):
        self.ax.set_title(self.name)
        x = x_y[0]
        y = x_y[1]
        xMax = max([np.max(x), abs(np.min(x))])
        yMax = max([np.max(y), abs(np.min(y))])
        # - Set axis when x or y is grater than current axis limit
        if xMax > self.axLimit or yMax > self.axLimit:
            if xMax > yMax and self.name == 'XY':
                self.axLimit = xMax + 0.1
            else:
                self.axLimit = yMax + 0.1
            # - 
            if self.name == 'XY':
                self.ax.axis((-self.axLimit, self.axLimit, -self.axLimit, self.axLimit))
            else:
                self.ax.axis((0, 2*pi, -self.axLimit, self.axLimit))
                
        self.ax.plot(x, y)
        self.legends.append(legend)    
        if legend:
            self.ax.legend(self.legends, loc='upper right')

        self.draw()


    def clear_plot(self):
        self.ax.cla() # - Clear plot
        self.axLimit = 1.1
        self.legends = []
        self.ax.axis((-self.axLimit, self.axLimit, -self.axLimit, self.axLimit))
        # Move left y-axis and bottim x-axis to centre, passing through (0,0)
        self.ax.spines['left'].set_position('center')
        self.ax.spines['bottom'].set_position('center')
        # Eliminate upper and right axes
        self.ax.spines['right'].set_color('none')
        self.ax.spines['top'].set_color('none')
        # Show ticks in the left and lower axes only
        self.ax.xaxis.set_ticks_position('none')
        self.ax.yaxis.set_ticks_position('none')
        self.draw()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
