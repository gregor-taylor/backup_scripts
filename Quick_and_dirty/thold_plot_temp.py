import matplotlib.pyplot as plt
import numpy as np
import csv
from tkinter.filedialog import askopenfilename
from tkinter import Tk
import matplotlib

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

Filename_DCR=askopenfilename(initialdir="Z:\\", title="Choose a dark count file?")
Filename_PCR = askopenfilename(initialdir="Z:\\", title="Choose a ph count file?")

power= 1.6e-3 
atten = 53
wav = 2328
phot_flux = calc_photon_flux(atten, wav, power)
eff_list=[]
DCR_list = []
tHold_list = []
with open(Filename_DCR) as csv_file:
    read_csv = csv.reader(csv_file)
    for row in read_csv:
        if len(row)>2:
        	if row[0] == 'Threshold (mV)':
        		pass
        	else:
        		tHold_list.append(row[0])
        		DCR_list.append(row[6])

PCR_list = []
with open(Filename_PCR) as csv_file:
    read_csv = csv.reader(csv_file)
    for row in read_csv:
        if len(row)>2:
        	if row[0] == 'Threshold (mV)':
        		pass
        	else:
        		PCR_list.append(row[6])

tHold_arr = np.asarray(tHold_list, dtype='float')
DCR_arr = np.asarray(DCR_list, dtype='float')
PCR_arr = np.asarray(PCR_list, dtype='float')

eff = calc_efficiency(PCR_arr, DCR_arr, phot_flux)

plt.plot(tHold_arr, eff,'rs', markersize=4)
plt.show()

