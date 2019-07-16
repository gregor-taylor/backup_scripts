from visa import *
import time
import os
import ThorlabsPM100 as PM
from GGT_funcs.py import write_local

'''
Settings to change

'''
FileName =  os.path.dirname(os.path.abspath(__file__))+"\\"+(time.ctime().replace(" ","_").replace(":","_"))+'_power_log.txt'
SleepTime = 2 # wait time in seconds

try:
    os.makedirs(os.path.dirname(FileName))
    print 'Directory',os.path.dirname(FileName),'created'
except OSError:
    print 'Directory',os.path.dirname(FileName),'exists'

power_meter_ID = "USB0::4883::32888::p0012119::0::INSTR"
power_meter_2_ID = "USB0::4883::32888::p0013440::0::INSTR"
w_length_pwr_m_1 = 2325
w_length_pwr_m_2 = 2325

write_err_flag = False
rm=ResourceManager()
with open(FileName, 'w+') as fname:
    writer_csv =  csv.writer(fname, delimiter=',')
    writer_csv.writerow(['Time', 'Power_1(W)', 'Power_2(W)'])
start_time = time.time()

PM100 = rm.open_resource(power_meter_ID)
print(PM100.query("*IDN?"))
pwr_m=PM.ThorlabsPM100(inst=PM100)

PM100_2=rm.open_resource(power_meter_2_ID)
print(PM100_2.query("*IDN?"))
pwr_m_2=PM.ThorlabsPM100(inst=PM100_2)
#pwr meter setup
#pwr_m.sense.average.count=3000 #must be set for low powers
#wavelengths
pwr_m.sense.correction.wavelength = w_length_pwr_m_1
pwr_m_2.sense.correction.wavelength= w_length_pwr_m_2
time.sleep(1)

while True:
    time_now = time.time()-start_time
    power = pwr_m.read
    power_2 = pwr_m_2.read
    combined_string = [str(time_now).strip(),+str(power).strip(),str(power_2).strip()]
    try:
        if write_err_flag == False:
            with open(FileName, 'w+') as fname:
                writer_csv =  csv.writer(fname, delimiter=',')
                writer_csv.writerow(combined_string)
        elif write_err_flag == True:
            write_local(combined_string)
    except IOError:
        write_local(combined_string)
        write_err_flag = True

    print('I have the power - '+str(time_now))
    time.sleep(SleepTime)

