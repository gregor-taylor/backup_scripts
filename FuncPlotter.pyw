#Function plotter

#Takes a python function as a string and evaluates it over a range given. Useful to visualise functions.

from PyQt5 import QtGui, QtCore, QtWidgets
import sys
import numpy as np
import matplotlib.pyplot as plt
import math

class FuncPlotter(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(FuncPlotter, self).__init__()
        self.initUi()
        
    def initUi(self):
        self.setGeometry(50, 50, 600, 150)
        self.setWindowTitle('Function Plotter')
        self.grid = QtWidgets.QGridLayout()
        self.setLayout(self.grid)

        func_lab = QtWidgets.QLabel(self)
        func_lab.setText('Function to plot: \n(Use x for variable, Python commands eg +,-,/,*\n,** etc and numpy commands preceded by np.)')
        self.grid.addWidget(func_lab,0,0)
        self.func_ip = QtWidgets.QLineEdit(self)
        self.grid.addWidget(self.func_ip,0,1)

        sv_lab = QtWidgets.QLabel(self)
        sv_lab.setText('Start value:')
        self.grid.addWidget(sv_lab,1,0)
        self.sv_ip = QtWidgets.QLineEdit(self)
        self.grid.addWidget(self.sv_ip,1,1)

        ev_lab = QtWidgets.QLabel(self)
        ev_lab.setText('End Value:')
        self.grid.addWidget(ev_lab,2,0)
        self.ev_ip = QtWidgets.QLineEdit(self)
        self.grid.addWidget(self.ev_ip,2,1)

        ss_lab = QtWidgets.QLabel(self)
        ss_lab.setText('Step size:')
        self.grid.addWidget(ss_lab,3,0)
        self.ss_ip = QtWidgets.QLineEdit(self)
        self.grid.addWidget(self.ss_ip,3,1)

        plt_ip = QtWidgets.QPushButton('Plot', self)
        plt_ip.clicked.connect(self.plt_it)
        self.grid.addWidget(plt_ip,4,0)

        self.show()

    def plt_it(self):
        try:
            func_to_use = self.func_ip.text()
            range_of_x = np.arange(float(self.sv_ip.text()),float(self.ev_ip.text())+float(self.ss_ip.text()),float(self.ss_ip.text()))
            y_list = []
            for i in range_of_x:
                x = i
                y = eval(func_to_use)
                y_list.append(y)
            y_arr = np.asarray(y_list)
            plt.plot(range_of_x, y_arr, 'o')
            plt.grid()
            plt.show()

        except ValueError:
            self.msg = QtWidgets.QMessageBox()
            self.msg.setIcon(QtWidgets.QMessageBox.Warning)
            self.msg.setText("Error with one of the entries!")
            self.msg.setWindowTitle("Error")
            self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            self.msg.show()
        
app = QtWidgets.QApplication(sys.argv)
GUI=FuncPlotter()
sys.exit(app.exec_())