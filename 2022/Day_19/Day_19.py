# -*- coding: utf-8 -*-
"""
    Created on Mon Dec 19 09:00:03 2022
    
    @author: MaxonIV
"""
import numpy as np
from itertools import permutations
# from more_itertools import distinct_permutations

# ==============================================================================
class Factory():
    
    def __init__(self, BP, max_minutes, prio_robot_list = [], verbose = False):
    
        self.minutes = 0
        self.max_minutes = max_minutes
        
        self.mats = {
            'ore': 0,
            'clay': 0,
            'obsidian': 0,
            'geode': 0
        }
        
        self.robots = {
            'Ore Robot': 1,
            'Clay Robot': 0,
            'Obsidian Robot': 0,
            'Geode Robot': 0
        }
        
        self.robot_mats = BP
        
        self.max_robots = dict(self.robots)
        
        self.max_robots['Geode Robot'] = np.inf
        
        for robot_type in list(self.max_robots):
            mat_type = robot_type.split(' ')[0].lower()
            
            for ref_robot, needed_mats in self.robot_mats.items():
                if mat_type in needed_mats:
                    self.max_robots[robot_type] = max(self.max_robots[robot_type], self.robot_mats[ref_robot][mat_type])
                    
        self.prio_robot_list = prio_robot_list
        
        self.verbose = verbose
        
    # ==========================================================================
    def reset(self, prio_robot_list = []):
    
        self.minutes = 0
        
        self.mats = {
            'ore': 0,
            'clay': 0,
            'obsidian': 0,
            'geode': 0
        }
        
        self.robots = {
            'Ore Robot': 1,
            'Clay Robot': 0,
            'Obsidian Robot': 0,
            'Geode Robot': 0
        }
            
        self.prio_robot_list = prio_robot_list
        
    # ==========================================================================
    def build_priority(self):
        
        if self.minutes in [5]:
            return 'Ore Robot'
        
        if self.minutes in [10]:
            return 'Clay Robot'
        
        if len(self.prio_robot_list) > 0:
            
            prio_robot = str(self.prio_robot_list[0].replace('HARD-', ''))
            
            can_prio = all([self.mats[robot_mat] >= quant for robot_mat, quant in self.robot_mats[prio_robot].items()])
            
            if can_prio:
                if self.verbose:
                    print(f'{prio_robot} prio')
                    print('_______________________________________________________')
                self.prio_robot_list.pop(0)
                return prio_robot
            
            elif 'HARD-' in self.prio_robot_list[0]:
                if self.verbose:
                    print(f'Hard priority requested for {prio_robot} and sufficient materials not met.')
                    print('Waiting...')
                    print('_______________________________________________________')
                return None
        
        if (self.mats['ore'] >= self.robot_mats['Geode Robot']['ore'] and
            self.mats['obsidian'] >= self.robot_mats['Geode Robot']['obsidian']):
            
            return 'Geode Robot'
        
        else:
            minutes_till_ore_for_geode_robot = np.ceil((self.robot_mats['Geode Robot']['ore'] - self.mats['ore'])/self.robots['Ore Robot'])
            if self.robots['Obsidian Robot'] > 0:
                minutes_till_obsidian_for_geode_robot = np.ceil((self.robot_mats['Geode Robot']['obsidian'] - self.mats['obsidian'])/self.robots['Obsidian Robot'])
            else:
                minutes_till_obsidian_for_geode_robot = np.inf
                
            make_ore = (minutes_till_obsidian_for_geode_robot <= 0)
            
            minutes_till_ore_for_geode_if_obsidian_is_made = np.ceil((self.robot_mats['Geode Robot']['ore'] - (self.mats['ore'] - self.robot_mats['Obsidian Robot']['ore']))/self.robots['Ore Robot'])
            
            minutes_till_geode_robot = max(minutes_till_ore_for_geode_robot, minutes_till_obsidian_for_geode_robot)
            
            
        if (not make_ore and self.robots['Obsidian Robot'] < self.max_robots['Obsidian Robot'] and
            minutes_till_ore_for_geode_if_obsidian_is_made <= minutes_till_geode_robot and
            self.mats['ore'] >= self.robot_mats['Obsidian Robot']['ore'] and
            self.mats['clay'] >= self.robot_mats['Obsidian Robot']['clay']):
            
            return 'Obsidian Robot'
        
        else:
            minutes_till_ore_for_obsidian_robot = np.ceil((self.robot_mats['Obsidian Robot']['ore'] - self.mats['ore'])/self.robots['Ore Robot'])
            if self.robots['Clay Robot'] > 0:
                minutes_till_clay_for_obsidian_robot = np.ceil((self.robot_mats['Obsidian Robot']['clay'] - self.mats['clay'])/self.robots['Clay Robot'])
            else:
                minutes_till_clay_for_obsidian_robot = np.inf
                
            make_ore = (minutes_till_clay_for_obsidian_robot <= 0)
            
            minutes_till_ore_for_geode_if_clay_is_made = np.ceil((self.robot_mats['Geode Robot']['ore'] - (self.mats['ore'] - self.robot_mats['Clay Robot']['ore']))/self.robots['Ore Robot'])
            minutes_till_ore_for_obsidian_if_clay_is_made = np.ceil((self.robot_mats['Obsidian Robot']['ore'] - (self.mats['ore'] - self.robot_mats['Clay Robot']['ore']))/self.robots['Ore Robot'])
            
            minutes_till_obsidian_robot = max(minutes_till_ore_for_obsidian_robot, minutes_till_clay_for_obsidian_robot)


        if (not make_ore and self.robots['Clay Robot'] < self.max_robots['Clay Robot'] and
            minutes_till_ore_for_geode_if_clay_is_made <= minutes_till_geode_robot and
            minutes_till_ore_for_obsidian_if_clay_is_made <= minutes_till_obsidian_robot and
            self.mats['ore'] >= self.robot_mats['Clay Robot']['ore']):
            
            return 'Clay Robot'
        
        else:
            minutes_till_ore_for_geode_if_ore_is_made = np.ceil((self.robot_mats['Geode Robot']['ore'] - (self.mats['ore'] - self.robot_mats['Ore Robot']['ore']))/(self.robots['Ore Robot'] + 1))
            minutes_till_ore_for_obsidian_if_ore_is_made = np.ceil((self.robot_mats['Obsidian Robot']['ore'] - (self.mats['ore'] - self.robot_mats['Ore Robot']['ore']))/(self.robots['Ore Robot'] + 1))
            minutes_till_ore_for_clay_if_ore_is_made = np.ceil((self.robot_mats['Clay Robot']['ore'] - (self.mats['ore'] - self.robot_mats['Ore Robot']['ore']))/(self.robots['Ore Robot'] + 1))
            
            minutes_till_clay_robot = np.ceil((self.robot_mats['Clay Robot']['ore'] - self.mats['ore'])/self.robots['Ore Robot'])
            # minutes_till_ore_robot = np.ceil((self.robot_mats['Ore Robot']['ore'] - self.mats['ore'])/self.robots['Ore Robot'])


        if ((make_ore and self.mats['ore'] >= self.robot_mats['Ore Robot']['ore']) or 
            (self.robots['Ore Robot'] < self.max_robots['Ore Robot'] and
             minutes_till_ore_for_geode_if_ore_is_made <= minutes_till_geode_robot and
             minutes_till_ore_for_obsidian_if_ore_is_made <= minutes_till_obsidian_robot and
             minutes_till_ore_for_clay_if_ore_is_made <= minutes_till_clay_robot and
             self.mats['ore'] >= self.robot_mats['Ore Robot']['ore'])):
            
            return 'Ore Robot'
        
        else:
            return None
            
    # ==========================================================================
    def Build_Robot(self, build_robot):
        
        self.robots[build_robot] += 1
        
        for robot_material in self.robot_mats[build_robot].keys():
            
            self.mats[robot_material] -= self.robot_mats[build_robot][robot_material]
        
    # ==========================================================================
    def propagate(self):

        self.minutes += 1
        
        if self.verbose:
            print(f'== Minute {self.minutes} ==')
        
        build_robot = self.build_priority()
        
        if build_robot:
            
            build_robot_type = build_robot.split(' ')[0].lower()
            
            for index, robot_material in enumerate(self.robot_mats[build_robot].keys()):
                if index == 0:
                    mat_text = f'{self.robot_mats[build_robot][robot_material]} {robot_material}'
                else:
                    mat_text += f' and {self.robot_mats[build_robot][robot_material]} {robot_material}'
            
            if build_robot_type != 'geode':
                action = 'collecting'
            else:
                action = 'cracking'
                
            if self.verbose:
                print(f'Spend {mat_text} to start building a {build_robot_type}-{action} robot.')
        
        for robot_type in self.robots.keys():
            mat_type = robot_type.split(' ')[0].lower()
            
            self.mats[mat_type] += self.robots[robot_type]
            
        if build_robot:
            self.Build_Robot(build_robot)
            
        if self.verbose:
            for robot_type in self.robots.keys():
                mat_type = robot_type.split(' ')[0].lower()
            
                if self.verbose and self.robots[robot_type] > 0:
                    if robot_type != build_robot:
                        minus_robot = 0
                    elif self.robots[robot_type] > 1:
                        minus_robot = 1
                    else:
                        continue
                        
                    
                    if robot_type != 'Geode Robot':
                        print(f'{self.robots[robot_type] - minus_robot} {mat_type}-collecting robot collects {self.robots[robot_type] - minus_robot} {mat_type}; you now have {self.mats[mat_type]} {mat_type}.')
                    else:
                        print(f'{self.robots[robot_type] - minus_robot} {mat_type}-cracking robot cracks {self.robots[robot_type] - minus_robot} {mat_type}(s); you now have {self.mats[mat_type]} open {mat_type}(s).')
            
            if build_robot:
                print(f'The new {build_robot_type.lower()}-{action} robot is ready; you now have {self.robots[build_robot]} of them.')
        
        if self.verbose:
            print('')

# ==============================================================================
    def propagate_to_max_time(self):
        
        
        for i in range(self.max_minutes):
            self.propagate()

# ==============================================================================
if __name__ == '__main__':
    
    BP_dic = {}
    case = ['Sample', 'Day_19']
    max_minute_scenarios = [24, 32]
    max_minutes = max_minute_scenarios[1]
    
    bypass_prio = False
    
    with open(f'{case[1]}_Input.txt', 'r') as inputs:
        Lines = inputs.readlines()
        
        for index, line_text in enumerate(Lines):
            line = line_text.replace('\n', '')
            
            colon_split = line.split(':')
            BP_num = colon_split[0].strip().replace('Blueprint', 'BP')
            period_split = colon_split[1].strip().split('.')
            
            BP_dic[BP_num] = {}
            
            for sentence in period_split:
                sentence_split = sentence.strip().replace('.', '').split(' ')
                
                if 'ore robot' in sentence:
                    BP_dic[BP_num]['Ore Robot'] = {
                        'ore': int(sentence_split[4])
                    }
                    
                elif 'clay robot' in sentence:
                    BP_dic[BP_num]['Clay Robot'] = {
                        'ore': int(sentence_split[4])
                    }
                    
                elif 'obsidian robot' in sentence:
                    BP_dic[BP_num]['Obsidian Robot'] = {
                        'ore': int(sentence_split[4]),
                        'clay': int(sentence_split[-2])
                    }
                    
                elif 'geode robot' in sentence:
                    BP_dic[BP_num]['Geode Robot'] = {
                        'ore': int(sentence_split[4]),
                        'obsidian': int(sentence_split[-2])
                    }
            
    
    Factory_dic = {}
    
    for BP in BP_dic.keys():
        Factory_dic[BP] = Factory(BP_dic[BP], max_minutes, verbose = False)
        
    total_quality_level = 0
    if max_minutes == 24:
        max_results = {
            'top quality level': 0
        }
    else:
        max_results = {
            'top quality level': 1
        }
    for BP_index, Factory_key in enumerate(Factory_dic.keys()):
        if BP_index + 1 > 3:
            continue
        max_results[Factory_key] = {
            'max geode': 0,
            'prio list': []
        }
        
        if not bypass_prio:
            # Problem 1
            # prio_ranges = [3, 1, 1, 2, 1]
            # Problem 2 Example
            # prio_ranges = [1, 1, 7, 0, 0]
            # Problem 2 
            prio_ranges = [1, 1, 3, 1, 0]
            seed_prio_list = []
            for _ in range(prio_ranges[0]):
                seed_prio_list.append('Ore Robot')
                
            for _ in range(prio_ranges[1]):
                seed_prio_list.append('HARD-Ore Robot')
                
            for _ in range(prio_ranges[2]):
                seed_prio_list.append('Clay Robot')
                
            for _ in range(prio_ranges[3]):
                seed_prio_list.append('Obsidian Robot')
                
            for _ in range(prio_ranges[4]):
                seed_prio_list.append('Geode Robot')
                
            for _ in range(6):
                seed_prio_list.append(None)
                
            full_prio_list_of_tups = list(permutations(seed_prio_list, 6))
            
            full_prio_list = []
            for prio_tup in full_prio_list_of_tups:
                
                prio_list = [element for element in list(prio_tup) if not isinstance(element, type(None))]
                
                if 'HARD-Ore' in prio_list and prio_list[0] != 'HARD-Ore':
                    prio_list.remove('HARD-Ore')
                    
                if prio_list not in full_prio_list:
                    full_prio_list.append(prio_list)
        else:
            full_prio_list = [[]]
            
        for case_num, prio_list in enumerate(full_prio_list):
            saved_prio_list = list(prio_list)
            # prio_list = ['Obsidian Robot', 'Ore Robot']
            # print(f'Starting case {case_num} of {len(full_prio_list)}: {prio_list}')
                        
            Factory = Factory_dic[Factory_key]
            
            Factory.reset(prio_list)
            
            Factory.propagate_to_max_time()
            
            if Factory.mats['geode'] >= max_results[Factory_key]['max geode']:
                if Factory.mats['geode'] == max_results[Factory_key]['max geode']:
                    if len(saved_prio_list) < len(max_results[Factory_key]['prio list']):
                        max_results[Factory_key]['prio list'] = saved_prio_list
                else:
                    max_results[Factory_key]['prio list'] = saved_prio_list
                        
                max_results[Factory_key]['max geode'] = Factory.mats['geode']
                    
            
        max_results[Factory_key]['quality level'] = int((BP_index + 1)*max_results[Factory_key]['max geode'])
        if max_minutes == 24:
            max_results['top quality level'] += max_results[Factory_key]['quality level']
        else:
            max_results['top quality level'] *= max_results[Factory_key]['max geode']
            
        print(f"Number of geodes produced by {Factory_key} factory: {max_results[Factory_key]['max geode']}")
        print(f"Current blueprint's quality level: {max_results[Factory_key]['quality level']}")
        print(f"Accumulated quality level: {max_results['top quality level']}")
        print('_______________________________________________________________')
        