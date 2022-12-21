# -*- coding: utf-8 -*-
"""
    Created on Wed Dec 21 01:13:32 2022
    
    @author: MaxonIV
"""
import numpy as np

# ==============================================================================
if __name__ == '__main__':
    
    case = ['Sample', 'Day_20']
    
    encrypted_list = []
    with open(f'{case[0]}_Input.txt', 'r') as inputs:
        Lines = inputs.readlines()
        
        for index, line_text in enumerate(Lines):
            line = line_text.replace('\n', '')
            
            encrypted_list.append(int(line))
            
    
    decryption_key = 811589153
    encrypted_list = [val*decryption_key for val in encrypted_list]
    
    for _ in range(2):
        index_list = list(range(len(encrypted_list)))
        print(encrypted_list)
        print(index_list)
        print('___________________________________________________________________')
        print('___________________________________________________________________')
        
        for actual_index in range(len(encrypted_list)):
            
            shifted_index = int(index_list[actual_index])
            
            for index, index_val in enumerate(index_list):
                if index_val <= shifted_index:
                    continue
                index_list[index] -= 1
                
            num_shift = encrypted_list.pop(shifted_index)
            
            rel_num_shift = num_shift + shifted_index
            
            if rel_num_shift < 0:
                if abs(rel_num_shift - 1) <= (len(encrypted_list) + 1):
                    
                    encrypted_list.insert(rel_num_shift, num_shift)
                    
                    index_list[actual_index] = len(index_list) + (rel_num_shift - 1)
                    
                    for index, index_val in enumerate(index_list):
                        if index_val < (len(index_list) + (rel_num_shift - 1)) or index == actual_index:
                            continue
                        index_list[index] += 1
                        
                        
                else:
                    mod_rel_num_shift = np.negative(abs(rel_num_shift)%len(encrypted_list))
                    
                    encrypted_list.insert(mod_rel_num_shift, num_shift)
                    
                    index_list[actual_index] = len(index_list) + (mod_rel_num_shift - 1)
                    
                    for index, index_val in enumerate(index_list):
                        if index_val < (len(index_list) + (mod_rel_num_shift - 1)) or index == actual_index:
                            continue
                        index_list[index] += 1
                        
                        
            else:
                if rel_num_shift < len(encrypted_list):
                    
                    encrypted_list.insert(rel_num_shift, num_shift)
                    
                    index_list[actual_index] = rel_num_shift
                    
                    for index, index_val in enumerate(index_list):
                        if index_val < rel_num_shift or index == actual_index:
                            continue
                        index_list[index] += 1
                        
                else:
                    mod_rel_num_shift = rel_num_shift%len(encrypted_list)
                    
                    encrypted_list.insert(mod_rel_num_shift, num_shift)
                    
                    index_list[actual_index] = mod_rel_num_shift
                    
                    for index, index_val in enumerate(index_list):
                        if index_val < mod_rel_num_shift or index == actual_index:
                            continue
                        index_list[index] += 1
            print(encrypted_list)
            print(index_list)
            print('___________________________________________________________________')
                        
    # zero_index = encrypted_list.index(0)
    # parse_from_zero_list = encrypted_list[zero_index:] + encrypted_list[:zero_index]
    # oneK_after_zero = parse_from_zero_list[1000%len(parse_from_zero_list)]
    # twoK_after_zero = parse_from_zero_list[2000%len(parse_from_zero_list)]
    # threeK_after_zero = parse_from_zero_list[3000%len(parse_from_zero_list)]
    
    # print(f'1000th number after zero is {oneK_after_zero}')
    # print(f'2000th number after zero is {twoK_after_zero}')
    # print(f'3000th number after zero is {threeK_after_zero}')
    # print(f'With the sum being: {oneK_after_zero + twoK_after_zero + threeK_after_zero}')
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    