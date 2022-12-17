# -*- coding: utf-8 -*-
"""
    Created on Fri Dec 16 10:38:02 2022
    
    @author: MaxonIV
"""
import json
import numpy as np

# ==============================================================================
def Rank_Data(Unranked_Data):
    '''
    Use:
        Provides a list that ranks all values of a provided list

    Inputs:
        1. Unranked_Data    - Array of values to be ranked

    Outputs:
        1. Ranked_Data      - Array of corresponding ranks
    '''
    Ranked_Data = []
    for Val in Unranked_Data:
        Ranked_Data.append(sum(i < Val for i in Unranked_Data))

    return Ranked_Data

# ==============================================================================
def Reverse_Valve_Search(search_valve, Valve_dic, valve_lists, old_valve_list):
    
    found = False
    new_valve_list = []
    
    for index, valve_list in enumerate(valve_lists):
        valve = valve_list[-1]
        old_valve_list.append(valve)
        
        for x_ref_valve in Valve_dic.keys():
            
            if x_ref_valve == valve or x_ref_valve in old_valve_list:
                continue
            
            if valve in Valve_dic[x_ref_valve]['to valves']:
                
                temp_valve_list = list(valve_list)
                temp_valve_list.append(x_ref_valve)
                
                new_valve_list.append(temp_valve_list)
                
                del temp_valve_list
                
                if x_ref_valve == search_valve:
                    found = True
            
            if found:
                break
            
        if found:
            break
                
    del valve_lists
    
    return found, new_valve_list

# ==============================================================================
def Calculate_Pressure_Released(complete_path_lists, full_path, FR_Valve_dic, old_valve_list):
    
    pre_results = {}
    
    for path in complete_path_lists:
        
        minutes = 0
        flow_rate = 0
        CPR = 0
        CPR_at_30 = 0
        PPR = 0
        FR_valve_count = 0
        
        if len(full_path) == 1:
            temp_complete_path = []
        else:
            temp_complete_path = list(full_path[:1])
        
        for valve in path:
            temp_complete_path.append(valve)
            
        title = f'{temp_complete_path[0]} -> {temp_complete_path[-1]}'
        
        for index, valve in enumerate(temp_complete_path):
            minutes += 1
            
            if index == 0:
                continue
            
            if valve in FR_Valve_dic.keys() and valve not in old_valve_list:
                minutes += 1
                FR_valve_count += 1
                
                flow_rate += FR_Valve_dic[valve]
                CPR += flow_rate
                
            if minutes == 30:
                CPR_at_30 = CPR
                PPR = CPR
                
        if minutes < 30:
            PPR = CPR + (30 - minutes)*flow_rate
                
        pre_results[title] = {
            'minutes': minutes,
            'flow rate': flow_rate,
            'current pressure released': CPR,
            '30 minute CPR': CPR_at_30,
            'projected pressure released': PPR,
            'FR valve count': FR_valve_count,
            'old valve list': old_valve_list,
            'full path': temp_complete_path
        }
    
    return pre_results

# ==============================================================================
def Select_Results(pre_results):
    
    path = ''
    max_PPR = 0
    for key in pre_results.keys():
        if pre_results[key]['projected pressure released'] > max_PPR:
            path = key
            max_PPR = pre_results[key]['projected pressure released']
    
    if path == '':
        raise Exception('Max CPR path was not found')
        
    else:
        Results = {
            path: pre_results[path]
        }
    
    return Results

# ==============================================================================
def Generate_Paths(Valve_dic, FR_Valve_dic, FR_values, path_start, old_valve_list_0):
    
    ranked_FR_values = Rank_Data(FR_values)
    
    complete_path_lists = []

    for ranked_FR in ranked_FR_values:
        
        old_valve_list = list(old_valve_list_0)
        
        FR_index = ranked_FR_values.index(ranked_FR)
        
        FR_value = FR_values[FR_index]
        
        for valve in Valve_dic.keys():
            if Valve_dic[valve]['flow rate'] == FR_value:
                break
            
        found = False
        valve_lists =  [[valve]]
        
        count = 0
        while not found and count < 100:
            count += 1
            found, valve_lists = Reverse_Valve_Search(path_start, Valve_dic, valve_lists, old_valve_list)
        
        if not found:
            print(f'Path not discovered for {valve}')
            
        else:
            path = list(reversed(valve_lists[-1]))
            
            if path[0] != path_start:
                raise Exception(f'First valve is not {path_start}')
            else:
                complete_path_lists.append(path)
            
    return complete_path_lists
# ==============================================================================
def Day_16_Seeder(Valve_dic, FR_Valve_dic, FR_values):
    
    Results = {
        'AA': {
            'minutes': 0,
            'flow rate': 0,
            'current pressure released': 0,
            '30 minute CPR': 0,
            'projected pressure released': 0,
            'FR valve count': 0,
            'old valve list': [],
            'full path': ['AA']
        }
    }
    
    while True:
        path = list(Results.keys())[0]
            
        path_start = path.split(' ')[-1]
        
        old_valve_list = Results[path]['old valve list']
        full_path = Results[path]['full path']
        FR_values_submit = list(FR_values)
        
        for old_valve in old_valve_list:
            if old_valve in FR_Valve_dic.keys():
                index = FR_values_submit.index(FR_Valve_dic[old_valve])
                
                FR_values_submit.pop(index)
        
        complete_path_lists = Generate_Paths(Valve_dic, FR_Valve_dic, FR_values_submit, path_start, old_valve_list)

        if len(complete_path_lists) > 1:
            pre_results = Calculate_Pressure_Released(complete_path_lists, full_path, FR_Valve_dic, old_valve_list)
            
            Results = Select_Results(pre_results)
            
            Results[list(Results)[0]]['old valve list'] = list(np.intersect1d(Results[list(Results)[0]]['full path'], list(FR_Valve_dic)))
            
            with open('Day_16_Results.json', 'w') as f:
                json.dump(Results, f, indent = 4)
            
            if len(np.intersect1d(old_valve_list, list(FR_Valve_dic))) >= len(list(FR_Valve_dic)) or Results[list(Results)[0]]['minutes'] >= 30:
                break
        else:
            break
    
    return Results
    
# ==============================================================================
if __name__ == '__main__':
    
    Valve_dic = {}
    FR_Valve_dic = {}
    FR_values = []
    case = ['Sample', 'Day_16']
    with open(f'{case[0]}_Input.txt', 'r') as inputs:
    # with open('Day_16_Input.txt', 'r') as inputs:
        Lines = inputs.readlines()
        
        for index, line_text in enumerate(Lines):
            line = line_text.replace('\n', '')
            
            semi_colon_split = line.split(';')
            
            equal_split = semi_colon_split[0].split('=')
            space_split = equal_split[0].split(' ')
            valve = space_split[1]
            FR = int(equal_split[1])
            if 'valves' in semi_colon_split[1]:
                remove_prefix = semi_colon_split[1].strip().split('lead to valves ')[-1]
                to_valves = remove_prefix.replace(' ', '').split(',')
            else:
                remove_prefix = semi_colon_split[1].strip().split('leads to valve ')[-1]
                to_valves = [remove_prefix.replace(' ', '')]
            
            Valve_dic[valve] = {
                'flow rate': FR,
                'to valves': to_valves
            }
            
            if FR > 0:
                FR_Valve_dic[valve] = FR
                FR_values.append(FR)
                
    Day_16_Seeder(Valve_dic, FR_Valve_dic, FR_values)
        
        
        
        
        
        
        
        
        
        
        
        
        
        