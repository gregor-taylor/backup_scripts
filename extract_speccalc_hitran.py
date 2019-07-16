#Extracts spectral line data from HITRAN and takes a solar spectral irradiance csv from ASTM
#Plots both on top of each other in the defined wavelength range.
#Define what moleceules you would like to see and the wavelength range.

import csv
import tkinter as tk
from tkinter.filedialog import askopenfilename
import numpy as np
import matplotlib.pyplot as plt
from  matplotlib import style
import matplotlib.ticker
style.use('fivethirtyeight_V2')

import hapi.hapi as hp

#def some tables of molecule numbers from HITRAN
molecule_dict = {'CO2':2, 'H2O':1, 'O3':3, 'O2':7}
#molecule_dict = {'NO':8}
atmospheric_comp = {'CO2':1.69e-3, 'H2O':0.106, 'O3':2.9e-7, 'O2':0.89230071,'CH4':7.62e-6, 'NO':1.38e-6}
source_list = []
lower_wav = 0.28
upper_wav = 4
#convert to wavenumbers
lower_wn = 1/(lower_wav*1e-4)
upper_wn = 1/(upper_wav*1e-4)
#CO2 first
for k,v in molecule_dict.items():
    hp.fetch(k,v, 1,upper_wn, lower_wn)
    source_list.append(k)
nu, coeff = hp.absorptionCoefficient_Lorentz(SourceTables=source_list, HITRAN_units=False, Diluent={'air':1.0})
nu, absorp = hp.absorptionSpectrum(nu, coeff, File="C:\\Users\\0901754t\\Documents\\Paper - LIDAR\\HITRAN2016\\spectra_op.txt")
wavelength= 1/(nu*1e-4)

#now get solar data
root = tk.Tk()
ASTM_file = askopenfilename(initialdir="Z:\\", title="Choose a file")
root.withdraw()
ASTM_wav=[]
ASTM_irr=[]
with open(ASTM_file) as csv_file:
    read_csv_file = csv.reader(csv_file, delimiter=',')
    for index, row in enumerate(read_csv_file):
        if index <3:
            pass
        else:
        	ASTM_wav.append(row[0])
        	ASTM_irr.append(row[1])
ASTM_wav_arr=(np.asarray(ASTM_wav, dtype='float'))/1e3
ASTM_irr_arr=np.asarray(ASTM_irr, dtype='float')

fig, ax1 = plt.subplots()
#plt.title('Solar irradiance and atmospheric absorption')
ax2 = ax1.twinx()
ax1.semilogx(ASTM_wav_arr, ASTM_irr_arr, 'r-', markersize=1, lw=2)
ax1.grid(True, which='both')
ax1.set_ylabel('Solar irradiance (W.m-2.nm-1)')
ax1.set_xlabel('Wavelength (μm)')
ax2.semilogx(wavelength, absorp, '-', markersize=1, lw=2)
ax2.set_xticks([0,1,2,3,4])
ax2.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
ax2.set_ylabel('Absorption')
ax2.set_zorder(1)
ax1.set_zorder(2)
ax1.patch.set_visible(False)
plt.grid()
plt.axvspan(2, 2.5, color='yellow', alpha=0.3)
plt.show()


