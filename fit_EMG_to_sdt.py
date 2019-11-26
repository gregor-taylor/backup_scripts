import numpy as np
import tkinter as tk
from tkinter import Tk, Frame, ttk, messagebox
from tkinter.filedialog import askopenfilename, askdirectory
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from  matplotlib import style
from sdtfile import SdtFile
from scipy.signal import correlate, savgol_filter
from scipy.special import erfc
from scipy.optimize import curve_fit
from math import sqrt
import csv
style.use('fivethirtyeight_V2')


def fit_exp_mod_gauss(times, counts, dt, plotting=False):
    #convert times to ps
    times=times/1e-12
    #use savitzky-golay poly to smooth data for guess
    smoothed_counts=savgol_filter(counts, 5, 4)
    #normalise by maxcounts then shift max counts bin to 0 - needed?
    max_ind = np.argmax(smoothed_counts)
    max_val = smoothed_counts[max_ind]
    time_shift=times[max_ind]
    times=times-time_shift
    smoothed_counts=smoothed_counts/max_val
    counts=counts/max_val

    dis_width=((np.where(smoothed_counts>=0.5))[0][-1]-(np.where(smoothed_counts>=0.5)[0][0]))
    #fwhm_guess =dis_width*dt
    #print(fwhm_guess)
    #work out where to start/end fittingbased on width
    start_p=max_ind-(5*dis_width)
    end_p=max_ind+(5*dis_width)
    sliced_times=times[start_p:end_p]

    popt, pcov = curve_fit(exp_mod_gauss, sliced_times, counts[start_p:end_p], p0=[1,-1, 1, 0])#,  bounds=((-10, 0, -np.inf),(10, 2000, np.inf)))
    fitted_func = exp_mod_gauss(sliced_times, popt[0], popt[1], popt[2], popt[3])

    centre=sliced_times[np.argmax(fitted_func)]+time_shift
    scale=np.amax(fitted_func)*max_val

    if plotting==True:
        fwhm=round(popt[2]*2.354820045, 3)
        print(fwhm+'ps')
        plt.plot(sliced_times+time_shift, counts[start_p:end_p]*max_val, 'x', markersize=6)
        plt.plot(sliced_times+time_shift,fitted_func*max_val/max(fitted_func),'r-', linewidth=2)
        plt.xlabel('Bin (ps)')
        plt.ylabel('Counts')
        plt.text(centre+10, scale, 'FWHM = '+str(fwhm)+'ps')
        plt.title('Datpoints and EMG fit')
        plt.legend(['Data', 'Fit'])
        plt.show()

    return centre, scale

def exp_mod_gauss(x, b, m, s, l):
    y = b*(0.5*l*np.exp(0.5*l*(2*m+l*s*s-2*x))*erfc((m+l*s*s-x)/(np.sqrt(2)*s)))
    return y
    #l=Lambda, s=Sigma, m=Mu, #b=

filename=askopenfilename(initialdir="C:\\", title="Choose an sdt file")
sdt_file=SdtFile(filename)

data = sdt_file.data[0][0]
adc_re=sdt_file.measure_info[0].adc_re
tac_r=sdt_file.measure_info[0].tac_r
tac_g=sdt_file.measure_info[0].tac_g
dt=tac_r/tac_g/adc_re
print(tac_r, tac_g, adc_re)
print(dt)
times=range(0,int(sdt_file.measure_info[0].adc_re))*dt

fit_exp_mod_gauss(times, data, dt, plotting=True)