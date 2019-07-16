import matplotlib.pyplot as plt
import numpy as np
import csv
from tkinter.filedialog import askopenfilename
from tkinter import Tk
import matplotlib

###SETUP
Tk().withdraw()
Filename_PCR=askopenfilename(initialdir="Z:\\", title="Choose a photon count file?")
Filename_DCR = askopenfilename(initialdir="Z:\\", title="Choose a dark count file?")
Filename_misc = askopenfilename(initialdir="Z:\\", title="Choose another count file?")
Atten = 6 #dB
power = 270e-6 #watts
wav = 2300 #nm

def calc_photon_flux(atten, wavelength, input_pwr):
        h = 6.626070040e-34
        c = 2.99792458e8
        out_pwr = (float(input_pwr))*(10**(-float(atten)/10)) 
        E_per_photon = h*(c/(int(wavelength)*1e-9)) #convert wlength to m 
        photon_flux = out_pwr/E_per_photon
       # print(photon_flux)
        return photon_flux

def calc_efficiency(P_counts,D_counts, photon_flux):
    eff = ((P_counts-D_counts)/photon_flux)*100
    return eff

bias_list = []
DCR_list = []
misc_count_list=[]
with open(Filename_DCR) as csv_file:
    read_csv = csv.reader(csv_file)
    for row in read_csv:
        if len(row)>2:
        	if row[0] == 'Time(s)':
        		pass
        	else:
        		bias_list.append(row[2])
        		DCR_list.append(row[3])

PCR_list = []
with open(Filename_PCR) as csv_file:
    read_csv = csv.reader(csv_file)
    for row in read_csv:
        if len(row)>2:
        	if row[0] == 'Time(s)':
        		pass
        	else:
        		PCR_list.append(row[3]) #assumes bias points the same

with open(Filename_misc) as csv_file:
    read_csv = csv.reader(csv_file)
    for row in read_csv:
        if len(row)>2:
            if row[0] == 'Time(s)':
                pass
            else:
                misc_count_list.append(row[3]) #assumes bias points the same


DCR_arr = np.asarray(DCR_list, dtype='float')
PCR_arr = np.asarray(PCR_list, dtype='float')
bias_arr = np.asarray(bias_list, dtype='float')
misc_arr = np.asarray(misc_count_list, dtype='float')

ph_flux = calc_photon_flux(Atten,wav,power)

Eff =calc_efficiency(PCR_arr, DCR_arr, ph_flux)
#print(Eff)

#graph things
fig, ax1 = plt.subplots()
ax1.set_xlabel('Bias (uA)')
ax1.set_ylabel('PCR (cps)')
ax1.plot(bias_arr, PCR_arr,'rs', markersize=4)
ax1.plot(bias_arr, DCR_arr, 'bs', markersize=4)
ax1.plot(bias_arr, misc_arr, 'ys', markersize=4)
ax1.legend(['After IP', 'Before OP', 'Coiled'], loc="upper left")
ax1.set_yscale('log')
#ax1.set_yticks(range(0,110,10))#set ticks for efficiency from 0 to 100
ax1.grid()#Grid on
#ax1.yaxis.set_major_locator(matplotlib.ticker.LinearLocator(10))
#ax2=ax1.twinx()
#ax2.set_ylabel('Counts (CPS)')
#ax2.semilogy(bias_arr, DCR_arr,'bs',markersize=4)
#ax2.legend(['DCR'], loc="lower right")
#ax2.yaxis.set_major_locator(matplotlib.ticker.LinearLocator(10))
''' #EFF PLOT
fig2, ax2 = plt.subplots()
ax2.plot(bias_arr, Eff)
ax2.set_xlabel('Bias (uA)')
ax2.set_ylabel('Efficiency (%)')
'''
plt.show()
