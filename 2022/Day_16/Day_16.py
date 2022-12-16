# -*- coding: utf-8 -*-
"""
    Created on Fri Dec 16 10:38:02 2022
    
    @author: MaxonIV
"""
Valve_dic = {}
FR_Valve_dic = {}

with open('Day_16_Input.txt', 'r') as inputs:
    Lines = inputs.readlines()
    
    for index, line_text in enumerate(Lines):
        line = line_text.replace('\n', '')
        
        semi_colon_split = line.split(';')
        
        equal_split = semi_colon_split[0].split('=')
        space_split = equal_split[0].split(' ')
        valve = space_split[1]
        FR = int(equal_split[1])
        
        remove_prefix = semi_colon_split[1].strip().split('lead to valves ')[-1]
        if ',' in remove_prefix:
            to_valves = remove_prefix.replace(' ', '').split(',')
        else:
            to_valves = [remove_prefix.replace(' ', '')]
        
        Valve_dic[valve] = {
            'flow rate': FR,
            'to valves': to_valves
        }
        
        if FR > 0:
            FR_Valve_dic[valve] = FR