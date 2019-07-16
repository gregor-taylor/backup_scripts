from visa import *
import time
import os

'''
Settings to change

'''
FileName =  os.path.dirname(os.path.abspath(__file__))+"\\"+(time.ctime().replace(" ","_").replace(":","_"))+'_power_vs_temp.txt'
SleepTime = 5 # wait time in seconds

try:
    os.makedirs(os.path.dirname(FileName))
    print 'Directory',os.path.dirname(FileName),'created'
except OSError:
    print 'Directory',os.path.dirname(FileName),'exists'

SIM900_port             = "GPIB0::2"
power_meter_ID = "USB0::4883::32888::p0012119::0::INSTR"

rm=ResourceManager()
fileHandle = open(FileName,'a')
fileHandle.write ('Time,T1(K),T2(K),T3(K),Power(W)\n')
fileHandle.close()

start_time = time.time()

SIM900 = rm.open_resource(SIM900_port)
SIM900_ID = SIM900.query('*IDN?')
print 'SIM900 ID :', SIM900_ID.strip()
SIM900 = rm.open_resource(SIM900_port)
SIM900.write('CONN 1,"xyx"')
SIM900_922 = SIM900.query('*IDN?')
print 'SIM922 :', SIM900_922.strip()
PM100 = rm.open_resource(power_meter_ID)
print(PM100.query("*IDN?"))
time.sleep(1)

while True:
    time_now = time.time()-start_time
    TEMP_922_A = SIM900.query('TVAL? 1')
    TEMP_922_B = SIM900.query('TVAL? 2')
    TEMP_922_C = SIM900.query('TVAL? 3')
    power = PM100.query("READ?")
    combined_string = str(time_now).strip()+', '+str(round(float(TEMP_922_A.strip()),2))+', '+str(round(float(TEMP_922_B.strip()),2))+', '+str(round(float(TEMP_922_C.strip()),2))+', '+power.strip()+'\n'
    fileHandle = open ( FileName, 'a' )
    fileHandle.write (combined_string)
    fileHandle.close()
    print('I am still alive')
    time.sleep(SleepTime)

