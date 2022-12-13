# -*- coding: utf-8 -*-
"""
    Created on Mon Dec 12 23:07:34 2022
    
    @author: MaxonIV
"""
import ast
import numpy as np

correct_pairs = []

# =============================================================================
def nest_until_match(input_1, input_2, index):

    if isinstance(input_1[index], int) and isinstance(input_2[index], list):
        input_1[index] = [input_1[index]]
        
        if input_2[index] and isinstance(input_2[index][0], list):
            nest_until_match(input_1[index], input_2[index], 0)
        
    elif isinstance(input_1[index], list) and isinstance(input_2[index], int):
        input_2[index] = [input_2[index]]
        
        if input_1[index] and isinstance(input_1[index][0], list):
            nest_until_match(input_1[index], input_2[index], 0)

# =============================================================================
def compare_lists(input_1, input_2, start_index = 0):
    
    len_1 = len(input_1)
    len_2 = len(input_2)
    
    rerun = False
    
    for index in range(start_index, min(len_1, len_2)):
        if isinstance(input_1[index], int) and isinstance(input_2[index], int):
            if input_1[index] < input_2[index]:
                list_checkout = True
                cont_to_next = False
                break
            elif input_1[index] == input_2[index]:
                continue
            else:
                list_checkout = False
                cont_to_next = False
                break
            
        elif isinstance(input_1[index], int) or isinstance(input_2[index], int):
            
            nest_until_match(input_1, input_2, index)
            
            rerun = True
            list_checkout = False
            cont_to_next = False
            break
            
    else:
        if len_1 < len_2:
            list_checkout = True
            cont_to_next = False
            
        elif len_1 == len_2:
            list_checkout = True
            cont_to_next = True
            
        elif len_1 > len_2:
            list_checkout = False
            cont_to_next = False
            
    return rerun, list_checkout, cont_to_next

# =============================================================================
def recursive_unnest(input_1, input_2, index):
    index += 1
    if isinstance(input_1[index], list) and isinstance(input_2[index], list):
        rerun, list_checkout, cont_to_next, index = unnest(input_1[index], input_2[index], 0)
        
        if not rerun and list_checkout and cont_to_next:
            if (index + 1) < min(len(input_1), len(input_2)):
                
                rerun, list_checkout, cont_to_next = recursive_unnest(input_1, input_2, index)
        
    elif isinstance(input_1[index], int) and isinstance(input_2[index], int):
        
        rerun, list_checkout, cont_to_next = compare_lists(input_1, input_2, index)
        
    elif isinstance(input_1[index], int) or isinstance(input_2[index], int):
        
        nest_until_match(input_1, input_2, index)
        
        rerun = True
        list_checkout = False
        cont_to_next = False
        
    return rerun, list_checkout, cont_to_next 

# =============================================================================
def unnest(input_1, input_2, index = 0):
    if input_1 and input_2 and isinstance(input_1[index], list) and isinstance(input_2[index], list):
        rerun, list_checkout, cont_to_next, index = unnest(input_1[index], input_2[index])
        
        if not rerun and list_checkout and cont_to_next:
            if (index + 1) < min(len(input_1), len(input_2)):
                
                rerun, list_checkout, cont_to_next = recursive_unnest(input_1, input_2, index)
        
    elif isinstance(input_1, list) and isinstance(input_2, list):
        rerun, list_checkout, cont_to_next = compare_lists(input_1, input_2)

    else:
        raise Exception(f'Inputs in unnest were not lists\n{input_1}\n{input_2}')
        
    return rerun, list_checkout, cont_to_next, index

# =============================================================================
def compare_inputs(input_1, input_2):
    
    len_1 = len(input_1)
    len_2 = len(input_2)
    
    for index in range(min(len_1, len_2)):
        if input_1 and input_2 and isinstance(input_1[index], list) and isinstance(input_2[index], list):
            rerun, list_checkout, cont_to_next, sub_index = unnest(input_1[index], input_2[index])
            
            if rerun:
                return rerun, False
            
        elif isinstance(input_1, list) and isinstance(input_2, list):
            rerun, list_checkout, cont_to_next = compare_lists(input_1, input_2, index)
            
            if rerun:
                return rerun, False
        else:
            raise Exception(f'Inputs in compare_inputs were not lists\n{input_1}\n{input_2}')
                
        if list_checkout and cont_to_next:
            continue
        else:
            return False, list_checkout
                    
    else:
        return False, (len_1 <= len_2)

# =============================================================================
with open('Day_13_Input.txt', 'r') as inputs:
    Lines = inputs.readlines()
    
    for index, line_text in enumerate(Lines):
        line = line_text.replace('\n', '')
        
        if index%3 == 0:
            input_1 = ast.literal_eval(line)
        elif index%3 == 1:
            input_2 = ast.literal_eval(line)
        else:
            while True:
                rerun, list_checkout = compare_inputs(input_1, input_2)
                
                if not rerun:
                    break
            
            if list_checkout:
                correct_pairs.append(index)
                
print(int(sum((np.array(correct_pairs) + 1)/3)))