# -*- coding: utf-8 -*-
"""
    Created on Mon Dec 12 12:18:47 2022
    
    @author: MaxonIV
"""

prio = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

sum_prio = 0
sum_group_prio = 0
group = ['','','']
with open('Day_3_Input.txt', 'r') as inputs:
    Lines = inputs.readlines()
    
    for index, line_text in enumerate(Lines):
        line = line_text.replace('\n', '')
        
        half = int(len(line)/2)
        
        comp1 = line[:half]
        comp2 = line[half:]
        
        shared = list(set(comp1) & set(comp2))
        
        sum_prio += (prio.index(shared[0]) + 1)
        
        if (index + 1) % 3 == 1:
            group[0] = line
        elif (index + 1) % 3 == 2:
            group[1] = line
        else:
            group[2] = line
            
            shared = list(set(group[0]) & set(group[1]) & set(group[2]))
            
            sum_group_prio += (prio.index(shared[0]) + 1)
            
            group = ['','','']
                
        
print(sum_prio)
print(sum_group_prio)