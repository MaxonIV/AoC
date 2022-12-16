# -*- coding: utf-8 -*-
"""
    Created on Thu Dec 15 16:41:39 2022
    
    @author: MaxonIV
"""
import numpy as np

structure = []
max_x = 0
max_y = 0
with open('Day_14_Input.txt', 'r') as inputs:
    Lines = inputs.readlines()
    
    for index, line_text in enumerate(Lines):
        line = line_text.replace('\n', '')
        
        line_split = line.split(' -> ')
        
        sub_structure = []
        for xy in line_split:
            xy_split = xy.split(',')
            x = int(xy_split[0])
            y = int(xy_split[1])
            sub_structure.append([x, y])
            
            max_x = max(x, max_x)
            max_y = max(y, max_y)
            
        structure.append(sub_structure)
        
# 0 = Empty
# 1 = Wall
# 8 = Sand

Map = np.zeros((max_y + 1, max_x + 1))

np.savetxt('Day_14_Map.txt', Map, fmt='%i')

for sub_structure in structure:
    for index, wall_start in enumerate(sub_structure[:-1]):
        wall_end = sub_structure[index + 1]
        
        if wall_start[1] == wall_end[1]:
            if wall_start[0] < wall_end[0]:
                for x in range(wall_start[0], wall_end[0] + 1):
                    Map[wall_start[1], x] = 1
                
            else:
                for x in range(wall_end[0], wall_start[0] + 1):
                    Map[wall_start[1], x] = 1
        else:
            if wall_start[1] < wall_end[1]:
                for y in range(wall_start[1], wall_end[1] + 1):
                    Map[y, wall_start[0]] = 1
                
            else:
                for y in range(wall_end[1], wall_start[1] + 1):
                    Map[y, wall_start[0]] = 1

np.savetxt('Day_14_Map.txt', Map, fmt='%i')