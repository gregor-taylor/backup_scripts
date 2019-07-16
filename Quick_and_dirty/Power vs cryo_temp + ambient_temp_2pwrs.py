from visa import *
import time
import os
import ThorlabsPM100 as PM

'''
Settings to change

'''
FileName =  os.path.dirname(os.path.abspath(__file__))+"\\"+(time.ctime().replace(" ","_").replace(":","_"))+'_power_vs_temp.txt'
SleepTime = 2 # wait time in seconds

try:
    os.makedirs(os.path.dirname(FileName))
    print 'Directory',os.path.dirname(FileName),'created'
except OSError:
    print 'Directory',os.path.dirname(FileName),'exists'

SIM900_port             = "GPIB0::2"
power_meter_ID = "USB0::4883::32888::p0012119::0::INSTR"
power_meter_2_ID = "USB0::4883::32888::p0008907::0::INSTR"

rm=ResourceManager()
fileHandle = open(FileName,'a')
fileHandle.write ('Time,T1(K),T2(K),T3(K),V1(V),V2(V),Power_1(W),Power_2(W)\n')
fileHandle.close()

start_time = time.time()

SIM900 = rm.open_resource(SIM900_port)
SIM900_ID = SIM900.query('*IDN?')
print 'SIM900 ID :', SIM900_ID.strip()
SIM900.write('xyxCONN 6,"xyx"')
SIM900_922 = SIM900.query('*IDN?')
print 'SIM922 :', SIM900_922.strip()
SIM900.write('xyxCONN 7,"xyx"')
#while True:
#    try:
#        SIM900_970 = SIM900.query('*IDN?')
#    except Exception:
#        continue
#    break
SIM900_970 = SIM900.query('*IDN?')
print 'SIM970 :', SIM900_970.strip()
PM100 = rm.open_resource(power_meter_ID)
print(PM100.query("*IDN?"))
pwr_m=PM.ThorlabsPM100(inst=PM100)

PM100_2=rm.open_resource(power_meter_2_ID)
print(PM100_2.query("*IDN?"))
pwr_m_2=PM.ThorlabsPM100(inst=PM100_2)
#pwr meter setup
#pwr_m.sense.average.count=3000 #must be set for low powers
pwr_m.sense.correction.wavelength = 2325

pwr_m_2.sense.correction.wavelength=2325
time.sleep(1)

while True:
    time_now = time.time()-start_time
    SIM900.write('xyxCONN 6,"xyx"')
    TEMP_922_A = SIM900.query('TVAL? 1')
    TEMP_922_B = SIM900.query('TVAL? 2')
    TEMP_922_C = SIM900.query('TVAL? 3')
    SIM900.write('xyxCONN7,"xyx"')
    DVM_1 = SIM900.ask('VOLT? 1,1')
    DVM_2 = SIM900.ask('VOLT? 2,1')
    power = pwr_m.read
    power_2 = pwr_m_2.read
    combined_string = str(time_now).strip()+', '+str(round(float(TEMP_922_A.strip()),2))+', '+str(round(float(TEMP_922_B.strip()),2))+', '+str(round(float(TEMP_922_C.strip()),2))+', '+str(DVM_1.strip())+', '+str(DVM_2.strip())+', '+str(power).strip()+', '+str(power_2).strip()+'\n'
    fileHandle = open ( FileName, 'a' )
    fileHandle.write (combined_string)
    fileHandle.close()
    print('I am still alive - '+str(time_now))
    time.sleep(SleepTime)

