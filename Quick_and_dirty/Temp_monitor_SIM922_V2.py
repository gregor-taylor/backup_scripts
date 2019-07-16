#=================================================================
#                                                                #
#  Name         :   Temp_monitor_SIM922.py                       #
#  Author       :   Chandra Mouli Natarajan                      #
#  Description  :   Reads and saves temperature with time        #
#                   new version                                  # 
#                                                                #
#=================================================================
from visa import *
import time
import os

'''
Settings to change
'''

BaseFolder    = r'Z:\Ramanator-PC\Kleanthis\measurements'
TargetFolder  = r'2017-11-21 2p3um NICT H3'
SampleBatch   = ''
SMANumber     = '1'
Comment       = 'Tc_warmup'

FileName=BaseFolder+'\\'+TargetFolder+'\\'+SampleBatch+'_SMA'+str(SMANumber)+'_I_V_'+Comment+'.txt'
#FileName=BaseFolder+'\\'+TargetFolder+'\\'+Comment+'.txt'

SleepTime = 0.2 # wait time in seconds

try:
    os.makedirs(os.path.dirname(FileName))
    print 'Directory',os.path.dirname(FileName),'created'
except OSError:
    print 'Directory',os.path.dirname(FileName),'exists'

SIM900_port             = "GPIB0::2"


number_of_measurements = 1

R = 100000
shunt_50ohm = 'No'

rm=ResourceManager()
fileHandle = open ( FileName, 'a' )
fileHandle.write ('Time\tT1(K)\tT2(K)\tT3(K)\n')
fileHandle.close()
 

number_of_measurements = 1

SIM900 = rm.open_resource(SIM900_port)
SIM900_ID = SIM900.query('*IDN?')
print 'SIM900 ID :', SIM900_ID.strip()

SIM900 = rm.open_resource(SIM900_port)

SIM900.write('CONN 1,"xyx"')
SIM900_922 = SIM900.query('*IDN?')
print 'SIM922 :', SIM900_922.strip()
SIM900.write('xyxCONN 2,"xyx"')
SIM900_928 = SIM900.query('*IDN?')
print 'SIM928:', SIM900_928.strip()
SIM900_928 = SIM900.write('VOLT 0.01')
SIM900_928 = SIM900.write('OPON')

initalTime = time.localtime()
print "Date and Time:", time.strftime("%d/%m/%y %H:%M:%S", initalTime)


R = 100000 #Bias Resistor
while True:
	try:
		currentTime = time.localtime()
		currentTimeString = time.strftime("%d/%m/%y %H:%M:%S", currentTime)

		time_difference = time.mktime(currentTime) - time.mktime(initalTime)
		timeDiffString = "%0.3f" % (time_difference/(60.0*60))

		SIM900.write('xyxCONN 1,"xyx"')

		TEMP_922_A = SIM900.query('TVAL? 1')
		TEMP_922_B = SIM900.query('TVAL? 2')
		TEMP_922_C = SIM900.query('TVAL? 3')
            
		
		SIM900.write('xyxCONN7,"xyx"')
		DVM_1 = SIM900.query('VOLT? 1,1')
		DVM_2 = SIM900.query('VOLT? 2,1')
		printString1 = DVM_2.strip()+','+str(float(DVM_1.strip())/R)+','+str((float(DVM_1.strip())-float(DVM_2.strip()))/R)+','+str((float(DVM_2.strip()))/((float(DVM_1.strip())-float(DVM_2.strip()))/R))
		printString = currentTimeString.strip()+', '+timeDiffString.strip()+', '+str(round(float(TEMP_922_A.strip()),2))+', '+str(round(float(TEMP_922_B.strip()),2))+', '+str(round(float(TEMP_922_C.strip()),2))
		print printString
		
		fileHandle = open ( FileName, 'a' )
		fileHandle.write (printString+','+printString1+'\n')
		fileHandle.close()
		time.sleep(SleepTime)
		
	except KeyboardInterrupt:
		SIM900.write('OPOF')
		print 'SIM900   :', SIM900.query('xyx*IDN?')
		print 'Program Stopped Abruptly'
		break
	except :
		print 'SIM900   :', SIM900.query('xyx*IDN?')
		raise
		break
