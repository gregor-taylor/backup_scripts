#Curve fitter

import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize
import csv
import tkinter as tk
from tkinter.filedialog import askopenfilename

def line(m,x,c):
    return (m*x)+c

def get_data(filename):
    data_1_list = []
    data_2_list = []
    with open(filename) as csv_file:
        read_csv = csv.reader(csv_file, delimiter=',')
        for index, row in enumerate(read_csv):
            if len(row)>0:
                if index==0:
                    pass
                else:            
                    data_1_list.append(float(row[1]))
                    data_2_list.append(float(row[2]))
    data_1 = np.asarray(data_1_list, dtype=float)
    data_2 = np.asarray(data_2_list, dtype=float)
    return data_1, data_2

#define
func_type = line

root = tk.Tk()
filename = askopenfilename(initialdir="Z:\\", title="Choose a file")
root.withdraw()

#get data from file
data_1, data_2 = get_data(filename)

#fit func
params, params_covariance = optimize.curve_fit(func_type, data_1, data_2)
#plot data 
plt.plot(data_1, data_2, 'bo')
#plot func
plt.plot(data_1, func_type(data_1, params[0],params[1]),'r')
plt.text(min(data_1), max(data_2), params)
plt.legend(['Data', 'Fit'],loc='lower right')
plt.show()


