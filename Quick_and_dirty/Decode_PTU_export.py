#Decode T2 export from Read_PTU.py

import matplotlib.pyplot as plt
import numpy as np
import csv
from tkinter.filedialog import askopenfilename
from tkinter import Tk
import matplotlib
import codecs

###SETUP
Tk().withdraw()
Filename = askopenfilename(initialdir="Z:\\", title="Choose a file")

DStart = False
#seperate datasets
Ch0_List = []
Ch1_List = []

co_time = 1000 #ps ()
seperate_dsets = False
sync_count=0
co_count = 0
co_list = []

with codecs.open(Filename, encoding='utf-16le') as csv_file:
    read_csv = csv.reader(csv_file, delimiter=' ')
    for row in read_csv:
        if len(row)>2:
        	if row[0] == "record#":
        		DStart=True
        	elif DStart == True:
        		if seperate_dsets == True:
        		    if row[1] == 'CHN':
        			    if row[2]=='0':
        				    Ch0_List.append(row[4])
        			    elif row[2]=='1':
        				    Ch1_List.append(row[4])
        		else:
        			if row[1] == 'CHN':
        				if row[2] == '0':
        					sync_count +=1
        					sync_time = float(row[4])
        				if row[2] == '1':
        					if float(row[4]) - sync_time <= co_time:
        						co_count+=1
        						co_list.append(row[4])
        	else:
        		pass

if seperate_dsets == True:
    ch0_counts=np.asarray(Ch0_List, dtype='float')
    ch1_counts=np.asarray(Ch1_List, dtype='float')


print (co_count, sync_count)
print(co_count/sync_count * 100)


