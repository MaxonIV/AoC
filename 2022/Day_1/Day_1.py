# -*- coding: utf-8 -*-
"""
    Created on Mon Dec 12 11:16:40 2022
    
    @author: MaxonIV
"""
import numpy as np

elf_calories = []

with open('Day_1_Input.txt', 'r') as inputs:
    Lines = inputs.readlines()
    
    for index, line_text in enumerate(Lines):
        line = line_text.replace('\n', '')
        if index == 0:
            elf_calories.append(int(line))
            
        elif line == '':
            elf_calories.append(0)
            continue
        
        else:
            elf_calories[-1] = elf_calories[-1] + int(line)
            
print(elf_calories[np.argmax(elf_calories)])

elf_calories.sort()

print(sum(elf_calories[-3:]))