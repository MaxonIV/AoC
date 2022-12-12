# -*- coding: utf-8 -*-
"""
    Created on Mon Dec 12 11:54:05 2022
    
    @author: MaxonIV
"""

Ref = {'A X': [1, 3],
       'A Y': [2, 6],
       'A Z': [3, 0],
       'B X': [1, 0],
       'B Y': [2, 3],
       'B Z': [3, 6],
       'C X': [1, 6],
       'C Y': [2, 0],
       'C Z': [3, 3]}

first_score = 0

second_score = 0

with open('Day_2_Input.txt', 'r') as inputs:
    Lines = inputs.readlines()
    
    for index, line_text in enumerate(Lines):
        line = line_text.replace('\n', '')
        
        first_score += sum(Ref[line])
        
        if line[-1] == 'X':
            if line[0] == 'A':
                p1 = 3
            elif line[0] == 'B':
                p1 = 1
            else:
                p1 = 2
            p2 = 0
        elif line[-1] == 'Y':
            if line[0] == 'A':
                p1 = 1
            elif line[0] == 'B':
                p1 = 2
            else:
                p1 = 3
            p2 = 3
        else:
            if line[0] == 'A':
                p1 = 2
            elif line[0] == 'B':
                p1 = 3
            else:
                p1 = 1
            p2 = 6
            
        second_score += (p1 + p2)

print(first_score)
print(second_score)