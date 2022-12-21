# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 23:38:58 2022

@author: mwidner
"""
from sympy.solvers import solve
from sympy import Symbol
# ==============================================================================
def check_all_values(input_str):
    
    allowed_params = ['X', ' ', '+', '-', '*', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '(', ')']
    
    return all([param in allowed_params for param in str(input_str)])

# ==============================================================================
if __name__ == '__main__':
    
    X = Symbol('X')
    BP_dic = {}
    case = ['Sample', 'Day_21']
    
    Monkeys = {}
    
    with open(f'{case[1]}_Input.txt', 'r') as inputs:
        Lines = inputs.readlines()
        
        for index, line_text in enumerate(Lines):
            line = line_text.replace('\n', '')
            
            colon_split = line.split(': ')
            
            try:
                Monkeys[colon_split[0]] = int(colon_split[1].strip())
            except:
                space_split = colon_split[1].strip().split(' ')
                
                Monkeys[colon_split[0]] = {
                    '1': space_split[0],
                    '2': space_split[2],
                    'operator': space_split[1]
                }
    # while True:
    #     for monkey_1 in list(Monkeys):
            
    #         if isinstance(Monkeys[monkey_1], int):
    #             for monkey_2 in list(Monkeys):
    #                 if isinstance(Monkeys[monkey_2], dict):
    #                     if monkey_1 == Monkeys[monkey_2]['1']:
    #                         Monkeys[monkey_2]['1'] = Monkeys[monkey_1]
    #                     elif monkey_1 == Monkeys[monkey_2]['2']:
    #                         Monkeys[monkey_2]['2'] = Monkeys[monkey_1]
                            
    #                     if isinstance(Monkeys[monkey_2]['1'], int) and isinstance(Monkeys[monkey_2]['2'], int):
    #                         Monkeys[monkey_2] = int(eval(f"({Monkeys[monkey_2]['1']} {Monkeys[monkey_2]['operator']} {Monkeys[monkey_2]['2']})"))
        
    #     if isinstance(Monkeys['root'], int):
    #         break
        
    # print(f"Root monkey will yell {Monkeys['root']}")
    
    Monkeys['humn'] = 'X'
    keep_going = True
    while keep_going:
        for monkey_1 in list(Monkeys):
            
            try:
                int(Monkeys[monkey_1])
                
                for monkey_2 in list(Monkeys):
                    if isinstance(Monkeys[monkey_2], dict):
                        if monkey_1 == Monkeys[monkey_2]['1']:
                            Monkeys[monkey_2]['1'] = Monkeys[monkey_1]
                        elif monkey_1 == Monkeys[monkey_2]['2']:
                            Monkeys[monkey_2]['2'] = Monkeys[monkey_1]
                            
                        if isinstance(Monkeys[monkey_2]['1'], int) and isinstance(Monkeys[monkey_2]['2'], int):
                            Monkeys[monkey_2] = int(eval(f"({Monkeys[monkey_2]['1']} {Monkeys[monkey_2]['operator']} {Monkeys[monkey_2]['2']})"))
            except:
                if isinstance(Monkeys[monkey_1], str):
                    if 'X' in Monkeys[monkey_1]:
                        for monkey_2 in list(Monkeys):
                            if isinstance(Monkeys[monkey_2], dict):
                                
                                if monkey_1 == Monkeys[monkey_2]['1']:
                                    Monkeys[monkey_2]['1'] = Monkeys[monkey_1]
                                    
                                elif monkey_1 == Monkeys[monkey_2]['2']:
                                    Monkeys[monkey_2]['2'] = Monkeys[monkey_1]
                                    
                elif isinstance(Monkeys[monkey_1], dict):
                    if isinstance(Monkeys[monkey_1]['1'], int) and isinstance(Monkeys[monkey_1]['2'], int):
                        Monkeys[monkey_2] = int(eval(f"{Monkeys[monkey_2]['1']} {Monkeys[monkey_2]['operator']} {Monkeys[monkey_2]['2']}"))
                        
                    elif all([check_all_values(Monkeys[monkey_1][key]) for key in list(Monkeys[monkey_1])]):
                        if monkey_1 != 'root':
                            Monkeys[monkey_1] = f"({Monkeys[monkey_1]['1']} {Monkeys[monkey_1]['operator']} {Monkeys[monkey_1]['2']})"
                        else:
                            Monkeys[monkey_1]['operator'] = '='
                            Monkeys[monkey_1] = f"({Monkeys[monkey_1]['1']} {Monkeys[monkey_1]['operator']} {Monkeys[monkey_1]['2']})"
                            print(Monkeys[monkey_1])
                            keep_going = False
                            
print(f'You should yell {solve(Monkeys[monkey_1])}')
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    