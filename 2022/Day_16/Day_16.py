# -*- coding: utf-8 -*-
"""
    Created on Fri Dec 16 10:38:02 2022
    
    @author: MaxonIV
"""
import json
import time
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
def Reverse_Valve_Search(search_valve, Valve_dic, valve_lists):
    
    found = False
    new_valve_list = []
    
    for index, valve_list in enumerate(valve_lists):
        valve = valve_list[-1]
        
        for x_ref_valve in Valve_dic.keys():
            
            if x_ref_valve == valve:
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
def Calculate_Pressure_Released(complete_path_lists, full_path, FR_Valve_dic):
    
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
            
            if valve in FR_Valve_dic.keys() and valve not in temp_complete_path[:index]:
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
            'full path': temp_complete_path
        }
    
    return pre_results

# ==============================================================================
def Calculate_Pressure_Released_v2(complete_pathway_lists, FR_Valve_dic, FR_hold_till_last_list):
    
    pre_results = []
    
    FR_Valve_list = list(FR_Valve_dic)
    
    for remove_valve in FR_hold_till_last_list:
        FR_Valve_list.remove(remove_valve)
    
    for path in complete_pathway_lists:
        
        minutes = 0
        flow_rate = 0
        CPR = 0
        PPR = 0
        
        for index, valve in enumerate(path):
            minutes += 1
            
            if valve in FR_Valve_list and valve not in path[:index]:
                
                CPR += flow_rate
                minutes += 1
                
                flow_rate += FR_Valve_dic[valve]
                CPR += flow_rate
                
            elif valve in FR_hold_till_last_list and all([check_valve in path[:index] for check_valve in FR_Valve_list]):
                CPR += flow_rate
                minutes += 1
                
                flow_rate += FR_Valve_dic[valve]
                CPR += flow_rate
                
            else:
                CPR += flow_rate
                
                
            if minutes == 30:
                PPR = CPR
                
        if minutes < 30:
            PPR = CPR + (30 - minutes)*flow_rate
            
        pre_results.append([PPR, minutes, CPR])
    
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
def Generate_Paths(Valve_dic, FR_Valve_dic, FR_values, path_start):
    
    ranked_FR_values = Rank_Data(FR_values)
    
    complete_path_lists = []

    for ranked_FR in ranked_FR_values:
        
        FR_index = ranked_FR_values.index(ranked_FR)
        
        FR_value = FR_values[FR_index]
        
        for valve in Valve_dic.keys():
            if Valve_dic[valve]['flow rate'] == FR_value:
                break
            
        found = False
        valve_lists =  [[valve]]
        
        count = 0
        while not found and count < 1000:
            count += 1
            found, valve_lists = Reverse_Valve_Search(path_start, Valve_dic, valve_lists)
        
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
            'full path': ['AA']
        }
    }
    
    while True:
        path = list(Results.keys())[0]
            
        path_start = path.split(' ')[-1]
        
        full_path = Results[path]['full path']
        FR_values_submit = list(FR_values)
        
        for valve_intersect in np.intersect1d(full_path, list(FR_Valve_dic)):
            index = FR_values_submit.index(FR_Valve_dic[valve_intersect])
            
            FR_values_submit.pop(index)
        
        complete_path_lists = Generate_Paths(Valve_dic, FR_Valve_dic, FR_values_submit, path_start)

        if len(complete_path_lists) > 1:
            pre_results = Calculate_Pressure_Released(complete_path_lists, full_path, FR_Valve_dic)
            
            Results = Select_Results(pre_results)
            
            try:
                with open('Day_16_Results.json', 'w') as f:
                    json.dump(Results, f, indent = 4)
            except:
                time.sleep(1)
                with open('Day_16_Results.json', 'w') as f:
                    json.dump(Results, f, indent = 4)
            
            if len(np.intersect1d(Results[list(Results)[0]]['full path'], list(FR_Valve_dic))) >= len(list(FR_Valve_dic)) or Results[list(Results)[0]]['minutes'] >= 30:
                break
        else:
            break
    
    return Results

# ==============================================================================
def Build_Valve_Pathways(initial_valve, Valve_dic, FR_Valve_dic, FR_values, FR_hold_till_last_list):
    
    # ==========================================================================
    def Build(valve_lists, FR_Valve_list):
        
        more_valves_to_add = True
        while more_valves_to_add:
            temp_valve_lists = []
            
            for valve_list in valve_lists:
                seed_list = list(valve_list)
                
                for valve in FR_Valve_list:
                    if valve not in seed_list:
                        temp_valve_list = list(seed_list)
                        temp_valve_list.append(valve)
                        temp_valve_lists.append(temp_valve_list)
            
            if len(temp_valve_lists) > 0:
                valve_lists = temp_valve_lists
            else:
                more_valves_to_add = False
                
        return valve_lists
        
    # ==========================================================================
    
    valve_lists = [[initial_valve]]
    
    FR_Valve_list = list(FR_Valve_dic)
    
    for remove_valve in FR_hold_till_last_list:
        FR_Valve_list.remove(remove_valve)
        
    valve_lists = Build(valve_lists, FR_Valve_list)
    
    if len(FR_hold_till_last_list) > 0:
        
        valve_lists = Build(valve_lists, FR_hold_till_last_list)
    
    return valve_lists

# ==============================================================================
def Map_Full_Pathways(valve_FR_pathways, Valve_dic):
    
    complete_pathway_lists = []
    
    for valve_FR_pathway in valve_FR_pathways:
        complete_path = [valve_FR_pathway[0]]
        for index, path_start in enumerate(valve_FR_pathway[:-1]):
            
            
            found = False
            valve_lists =  [[valve_FR_pathway[index + 1]]]
        
            count = 0
            while not found and count < 1000:
                count += 1
                found, valve_lists = Reverse_Valve_Search(path_start, Valve_dic, valve_lists)
        
            if not found:
                print(f'Path not discovered for {valve}')
                
            else:
                path = list(reversed(valve_lists[-1]))
                
                complete_path.extend(path[1:])
            

        complete_pathway_lists.append(complete_path)
        
    return complete_pathway_lists
    
# ==============================================================================
if __name__ == '__main__':
    
    Valve_dic = {}
    FR_Valve_dic = {}
    FR_values = []
    case = ['Sample', 'Day_16']
    with open(f'{case[1]}_Input.txt', 'r') as inputs:
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
                
    # Day_16_Seeder(Valve_dic, FR_Valve_dic, FR_values)
    
    # valve_lists = Brute_with_Logic('AA', Valve_dic, FR_Valve_dic, FR_values)
    
    # desired_keys = list(FR_Valve_dic)[:3]
    # sub_FR_Valve_dic = {key:value for key, value in FR_Valve_dic.items() if key in desired_keys}
    
    FR_hold_threshold = 16
    FR_hold_till_last_list = []
    
    for valve in FR_Valve_dic.keys():
        if FR_Valve_dic[valve] <= FR_hold_threshold:
            for index, compare_valve in enumerate(FR_hold_till_last_list):
                if FR_Valve_dic[valve] < FR_Valve_dic[compare_valve]:
                    FR_hold_till_last_list.insert(index, valve)
                    break
            else:
                FR_hold_till_last_list.append(valve)
    
    valve_FR_pathways = Build_Valve_Pathways('AA', Valve_dic, FR_Valve_dic, FR_values, FR_hold_till_last_list)
    
    complete_pathway_lists = Map_Full_Pathways(valve_FR_pathways, Valve_dic)
    
    pre_results = Calculate_Pressure_Released_v2(complete_pathway_lists, FR_Valve_dic, FR_hold_till_last_list)
        
    max_PR = 0
    for index, pre_result in enumerate(pre_results):
        if pre_result[0] > max_PR:
            max_PR = pre_result[0]
            max_PR_index = index
    
    print(max_PR_index, max_PR)
            
    # sample_path = ['AA', 'DD', 'CC', 'BB', 'AA', 'II', 'JJ', 'II', 'AA', 'DD', 'EE', 'FF', 'GG', 'HH', 'GG', 'FF', 'EE', 'DD', 'CC']
        
    # count = 0
    # length = 18
    # for index, pathway in enumerate(complete_pathway_lists):
    #     if sample_path[:length] == pathway[:length]:
    #         count += 1
            
    # print(count)
        
        
        
        
        
        
        
        
        