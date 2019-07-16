# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 10:25:45 2018

Gets DCs and PCs for a given bias for a variety of attenuations.

G Taylor
@author: 0901754T
"""

from visa import *
import time
import os
import csv

rm=ResourceManager()
Op_Attn_1_Address       = "GPIB0::10"
Op_Attn_2_Address       = "GPIB0::14"
Pulse_Counter_Address   = "GPIB0::3"
SIM900_port             = "GPIB0::2"

FilePath = r'S:\QSG\Ramanator-PC\Gregor\DFTS\W3 B2\QE\\'
Date = '30_03_2018'
Device = 'C7'
SM = '3'
Wavelength = '1550' #nm
Optical_Power = '1' #uW
Bias = '3.1-3.8'
Count = 'No_POLARISATION_3_attens'	

Attenuations = [80, 84, 88] #dBs - divisble by 2
Start_Voltage = 3.1
Max_Voltage = 3.8
Voltage_step_size = 0.05


h = 6.626070040e-34
c = 2.99792458e8

FileName = FilePath+'QE_'+Device+'_'+SM+'_'+Wavelength+'_nm_'+Optical_Power+'_uw_'+Bias+'_'+Count+'_Count_'+Date+'.txt'

try:
    os.makedirs(os.path.dirname(FileName))
    print ('Directory',os.path.dirname(FileName),'created')
except OSError:
    print ('Directory',os.path.dirname(FileName),'exists')

SIM900 = rm.open_resource(SIM900_port)
Pulse_Cnt = rm.open_resource(Pulse_Counter_Address)
Op_Attn_1 = rm.open_resource(Op_Attn_1_Address)
Op_Attn_2 = rm.open_resource(Op_Attn_2_Address)

def calc_photon_flux(atten, wavelength, input_pwr):
    out_pwr = (input_pwr*1e-6)*(10**(-atten/10)) #Watts
    E_per_photon = h*(c/(int(wavelength)*1e-9)) #convert wlength to m 
    photon_flux = out_pwr/E_per_photon
    return photon_flux

def calc_efficiency(P_counts,D_counts, photon_flux):
    eff = ((P_counts-D_counts)/photon_flux)*100
    return eff

for atten in Attenuations:
    Voltage = Start_Voltage
    with open(FileName, 'a') as file_handle:
        photon_flux = calc_photon_flux(float(atten), int(Wavelength), float(Optical_Power))
        writer_csv = csv.writer(file_handle, delimiter=',')
        writer_csv.writerow(['ATTENUATION', atten, photon_flux ])
        print('Taking measurement for a photon flux of '+str(photon_flux)+' Photons/S')
        Pulse_Cnt.write('*IDN?')    
        print ('Pulse_Cnt   :', Pulse_Cnt.read())
        Pulse_Cnt.write(':INP1:COUP AC;IMP 50 OHM')
             
        print ('Op_Attn_1 :', Op_Attn_1.ask("*IDN?"))
        Op_Attn_1.write(':INP:WAV 940 NM')    
        print ('Op_Attn_1 :', Op_Attn_1.ask(":INP:WAV?"))

        print ('Op_Attn_2 :', Op_Attn_2.ask("*IDN?"))
        Op_Attn_2.write(':INP:WAV 940 NM')    
        print ('Op_Attn_2 :', Op_Attn_2.ask(":INP:WAV?"))
        time.sleep(1)

        Attn_input = ':INP:ATT '+ str(atten/2) + ' dB'
        Op_Attn_1.write(Attn_input)
        Op_Attn_2.write(Attn_input)
        while Max_Voltage > Voltage:

            SIM900.write('SRST')
            SIM900_In = SIM900.ask('*IDN?')
            print ('SIM900 In:', SIM900_In.strip(), '\n')
            counts_cont = []

            #Not sure why this section has to be here but it timesout if it's not
            SIM900.write('CONN 1,"xyx"')
            TEMP_2_1 = SIM900.ask('TVAL? 1')
            VOLT_2_1 = SIM900.ask('VOLT? 1')
            print 'SIM 922 - Temperature 2', TEMP_2_1.strip()
            print 'SIM 922 - Voltage 2', VOLT_2_1.strip(), '\n'

            #Set voltage on SIM_900
            SIM900.write('xyxCONN 2,"xyx"')
            SIM900_4 = SIM900.ask('*IDN?')

            Set_Voltage_CMD = 'VOLT ' + str(Voltage)
            print (Set_Voltage_CMD)

            SIM900.write(Set_Voltage_CMD)
            SIM900.write('OPON')
            DVS_4 = SIM900.ask('VOLT?')
            print ('SET Volt SRC 4', DVS_4.strip(), '\n')
            
            SIM900.write('xyx*IDN?')
            SIM900_In = SIM900.read()
            print ('SIM900 In:', SIM900_In.strip(), '\n')
            
            #DC
            Op_Attn_1.write(':OUTP:STAT OFF')
            while len(counts_cont) < 5:
                Pulse_Cnt.write('SENS:TOT:ARM:STOP:TIM 1')
                counts_cont.append(float(Pulse_Cnt.ask("READ?")))
                time.sleep(1)
            DC_val = sum(counts_cont)/5
            #PC
            Op_Attn_1.write(':OUTP:STAT ON')
            counts_cont = []
            time.sleep(3) #settle counts down
            while len(counts_cont) < 5:
                Pulse_Cnt.write('SENS:TOT:ARM:STOP:TIM 1')
                counts_cont.append(float(Pulse_Cnt.ask("READ?")))
                time.sleep(1)
            PC_val = sum(counts_cont)/5
            eff = calc_efficiency(PC_val, DC_val, photon_flux)
            writer_csv.writerow([Voltage, DC_val, PC_val, eff])
            Voltage = Voltage + Voltage_step_size
            #Reset everything to OFF
            Op_Attn_1.write(':OUTP:STAT OFF')
            SIM900.write('OPOFF')


            
    
    
    

    
