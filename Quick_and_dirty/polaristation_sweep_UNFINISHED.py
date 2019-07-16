# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 10:16:15 2018

@author: 0901754T
"""

from visa import *
import time
import os
rm=ResourceManager()

polarisation_controller_Address = ""
Pulse_Counter_Address   = "GPIB0::3"
SIM900_port             = "GPIB0::2"

FilePath = r'Z:\Ramanator-PC\Gregor\DFTS\W3 C7\QE\\'
Date = '18_01_2018'
Device = 'C7'
SM = '1'
Wavelength = '1550_nm'
Count = 'HPB168F CW laser_w_polariser'	


FileName = FilePath+Device+'_'+SM+'_'+Count+'_Polarisation_dependence_'+Date+'.txt'

try:
    os.makedirs(os.path.dirname(FileName))
    print 'Directory',os.path.dirname(FileName),'created'
except OSError:
    print 'Directory',os.path.dirname(FileName),'exists'
    
SIM900 = rm.open_resource(SIM900_port)
Pulse_Cnt = rm.open_resource(Pulse_Counter_Address)
Pol_Cont = rm.open_resource(polarisation_controller_Address)

angle = range(1,181)