#Plot .sdt files from b&H card
#G Taylor
#

import tkinter as tk
from tkinter.filedialog import askopenfilename
from sdtfile import SdtFile
import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize


start_gate=300

def get_max(data_array):
    index_max = np.argmax(data_array, axis=0)
    max_val = data_array[index_max]
    return index_max, max_val

def gauss(B,x):
    #B is a list of m, stddev, max, offset
    #constants worked out first for clarity
    a = B[3]+B[2]/(B[1]*np.sqrt(2*np.pi))
    b = B[0]
    c = B[1]
    y = a*np.exp(-(x-b)**2/(2*c**2))
    return y 

def errorfunc(B, x, y):
    return y-gauss(B,x)

filename = askopenfilename(initialdir="Z:\\", title="Choose an sdt file")

sdt=SdtFile(filename)
data=sdt.data[0][0][start_gate:]


m, max_val = get_max(data)
B = [m, 0.55,max_val, 0]
x = np.arange(1,len(data)+1)

p0 = [m,1.,max_val,1.]
fit = optimize.leastsq(errorfunc, p0, args=(x,data))
fitted_curve = gauss(fit[0], x)

#time_per_bin=abs(sdt.times[0][1])
time_per_bin = 0.203


print(fit)

plt.plot(data, 'b.')
plt.plot(x, fitted_curve,'r-')
print(fit[0][1])
FWHM = (2.354820045*fit[0][1])*time_per_bin #ps #DOESN'T WORK
print(FWHM)
plt.title('IRF')
plt.xlabel('Time ('+str(time_per_bin)+'ps per bin)')
plt.ylabel('Counts')
plt.show()
