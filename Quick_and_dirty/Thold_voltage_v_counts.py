#Vary threshold V and check counts.

from visa import *
import time
import os
import csv

rm=ResourceManager()
Pulse_Counter_Address   = "GPIB0::18"
Dev = 'G1'
Comments = 'PC_7.5uA_80dB_1.51mW'
min_v = 20 #mv
max_v = 150 #mv
v_step = 10 #mv

FileName='Threshold_V_vs_counts_'+Dev+Comments+'.txt'
Pulse_Cnt = rm.open_resource(Pulse_Counter_Address)
try:
    os.makedirs(os.path.dirname(FileName))
    print ('Directory',os.path.dirname(FileName),'created')
except OSError:
    print ('Directory',os.path.dirname(FileName),'exists')

with open(FileName, 'a') as file_to_write:
    writer_csv = csv.writer(file_to_write, delimiter=',')
    writer_csv.writerow(['Threshold (mV)','Count1','Count2','Count3','Count4','Count5','CountAverage'])
    for v in range(min_v, max_v+v_step, v_step):
        counts_cont = []
        Pulse_Cnt.write('SENS:EVEN1:LEV:ABS '+'-'+str((v/1000)))
        while len(counts_cont) < 5:
            Pulse_Cnt.write('SENS:TOT:ARM:STOP:TIM 1')
            counts_cont.append(float(Pulse_Cnt.ask("READ?")))
            time.sleep(1)
        Av_val = sum(counts_cont)/5
        data_to_write = [v]+counts_cont+[Av_val]
        writer_csv.writerow(data_to_write)

