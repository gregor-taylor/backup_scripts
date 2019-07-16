# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 11:45:10 2018

@author: 0901754T
"""

#FWHM function
def FWHM(data_array, ns_per_div): 
    HM = (np.round(np.amax(data_array, axis=0),-3)/2)     #This round not neccessary, just makes number easier
    rounded_array = np.round(data_array, -3) 
    index_max= np.argmax(data_array, axis=0)
 #Rounds array to find approx half max
    how_close_neg, index_HM_neg, how_close_pos, index_HM_pos = find_closest(rounded_array, HM,index_max)
    FWHM = index_HM_pos-index_HM_neg
    return FWHM, index_max, data_array[index_max]

#Function takes an array or list, a number that you want to be close to (the max), the index of this max value then works out the closest number and index
#above and below it.
def find_closest(list_of_num, number_to_be_close_to, index_of_max):
    j_neg=10000 #this is the minimum distance away it can be, just to start with.
    j_pos=10000
    j_index_pos=0
    j_index_neg=0
    for index, number in enumerate(list_of_num):
        if number>0:
            if (index_of_max-1000)<index<index_of_max: #only the peak that is around the max if there's more than 1, if it's above 1ns away then it's shite anyway
                sub_neg = abs(number_to_be_close_to-number)
                if sub_neg<j_neg:
                    j_neg=sub_neg
                    j_index_neg = index
            if (index_of_max+1000)>index>index_of_max:
                sub_pos = abs(number_to_be_close_to - number)
                if sub_pos<j_pos:
                    j_pos=sub_pos
                    j_index_pos = index  
    return j_neg, j_index_neg, j_pos, j_index_pos               
            