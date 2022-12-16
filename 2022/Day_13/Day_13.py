# -*- coding: utf-8 -*-
"""
    Created on Mon Dec 12 23:07:34 2022
    
    @author: MaxonIV
"""
import ast
import numpy as np
# import sys
# import inspect

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
            rerun, list_checkout, cont_to_next = compare_lists(input_1[index], input_2[index])
            
            if rerun or not list_checkout:
                break
            elif list_checkout and not cont_to_next:
                break
            elif list_checkout and cont_to_next:
                continue
            
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
    if input_1 and input_2 and isinstance(input_1[index], list) and isinstance(input_2[index], list):
        rerun, list_checkout, cont_to_next, index = recursive_unnest(input_1[index], input_2[index], 0)

        if not rerun and list_checkout and cont_to_next:
            if (index + 1) < min(len(input_1), len(input_2)):
                index += 1
                rerun, list_checkout, cont_to_next, index = recursive_unnest(input_1, input_2, index)
                
            elif len(input_1) > len(input_2):
                list_checkout = False
                cont_to_next = False
        
    elif isinstance(input_1, list) and isinstance(input_2, list):
        
        rerun, list_checkout, cont_to_next = compare_lists(input_1, input_2)
        
    # elif isinstance(input_1[index], int) or isinstance(input_2[index], int):
        
    #     nest_until_match(input_1, input_2, index)
        
    #     rerun = True
    #     list_checkout = False
    #     cont_to_next = False
        
    return rerun, list_checkout, cont_to_next, index

# # =============================================================================
# def unnest(input_1, input_2, index = 0):

#     if input_1 and input_2 and isinstance(input_1[index], list) and isinstance(input_2[index], list):
#         rerun, list_checkout, cont_to_next, index = unnest(input_1[index], input_2[index])
        
#         if not rerun and list_checkout and cont_to_next:
#             if (index + 1) < min(len(input_1), len(input_2)):
#                 index += 1
#                 rerun, list_checkout, cont_to_next, index = recursive_unnest(input_1, input_2, index)
                
#             elif len(input_1) > len(input_2):
#                 list_checkout = False
#                 cont_to_next = False
        
#     elif isinstance(input_1, list) and isinstance(input_2, list):
        
#         rerun, list_checkout, cont_to_next = compare_lists(input_1, input_2)
        
#     return rerun, list_checkout, cont_to_next, index

# =============================================================================
def compare_inputs(input_1, input_2):
    
    len_1 = len(input_1)
    len_2 = len(input_2)
    
    for index in range(min(len_1, len_2)):
        if input_1 and input_2 and isinstance(input_1[index], list) and isinstance(input_2[index], list):
            rerun, list_checkout, cont_to_next, sub_index = recursive_unnest(input_1[index], input_2[index], 0)
            
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
if __name__ == '__main__':
    
    div_packets = ['[[2]]', '[[6]]']
    packet_list = []
    
    # file1 = open('check.txt', 'w')
    # file2 = open('13b.txt', 'w')
    with open('Day_13_Input.txt', 'r') as inputs:
    # with open('sample.txt', 'r') as inputs:
    # with open('13b.txt', 'r') as inputs:
        Lines = inputs.readlines()
        
        for line_num, line_text in enumerate(Lines):
            line = line_text.replace('\n', '')
    # # ==========================================================================
    #         # if line_num < 348 or line_num > 350:
    #         #     continue
            
    #         if line_num%3 == 0:
    #             input_1 = ast.literal_eval(line)
    #             # file1.write(f'{line}\n')
    #         elif line_num%3 == 1:
    #             input_2 = ast.literal_eval(line)
    #             # file1.write(f'{line}\n')
    #         else:
    #             while True:
    #                 rerun, list_checkout = compare_inputs(input_1, input_2)
                    
    #                 if not rerun:
    #                     break
                
    #             if list_checkout:
    #                 correct_pairs.append(line_num)
    #                 # file1.write('\n')
    #             # else:
    #                 # file1.write('x\n')
                    
    #     while True:
    #         rerun, list_checkout = compare_inputs(input_1, input_2)
            
    #         if not rerun:
    #             break
        
    #     if list_checkout:
    #         correct_pairs.append(line_num)
    #         # file1.write('\n')
    #     # else:
    #     #     file1.write('x\n')
                        
    # print(int(sum((np.array(correct_pairs) + 1)/3)))
    # # file1.close()
    # # ==========================================================================
            if line == '':
                continue
            # file2.write(line_text)
            packet_list.append(line)
    # file2.write('\n')
    for div_packet in div_packets:
        
        # file2.write(f'{div_packet}\n')
        packet_list.append(div_packet)
    # file2.close()
    # ==========================================================================
    
    while True:
        shift_list = []
        for index, packet in enumerate(packet_list[:-1]):
            packet_1 = ast.literal_eval(packet)
            packet_2 = ast.literal_eval(packet_list[index + 1])
            
            while True:
                rerun, list_checkout = compare_inputs(packet_1, packet_2)
                
                if not rerun:
                    break
            
            if not list_checkout:
                shift_list.append(index)
                
        if len(shift_list) == 0:
            break
        else:
            # print(len(shift_list))
            skip = False
            
            for index, shift_index in enumerate(shift_list):
                if skip:
                    skip = False
                    continue
                
                if (index + 1 < len(shift_list) and 
                    shift_index + 1 == shift_list[index + 1]):
                    skip = True
                    
                pop = packet_list.pop(shift_index)
                packet_list.insert(shift_index + 1, pop)
                
        # file2 = open('13b.txt', 'w')
        # for packet in packet_list:
        #     file2.write(f'{packet}\n')
        # file2.close()
          

        # print('***************************************************************')
        # print(f'check:          {sys.getsizeof(check)}')
        # print(f'correct_pairs:  {sys.getsizeof(correct_pairs)}')
        # print(f'div_packet:     {sys.getsizeof(div_packet)}')
        # print(f'div_packets:    {sys.getsizeof(div_packets)}')
        # print(f'index:          {sys.getsizeof(index)}')
        # print(f'line:           {sys.getsizeof(line)}')
        # print(f'line_num:       {sys.getsizeof(line_num)}')
        # print(f'line_text:      {sys.getsizeof(line_text)}')
        # print(f'Lines:          {sys.getsizeof(Lines)}')
        # print(f'list_checkout:  {sys.getsizeof(list_checkout)}')
        # print(f'packet:         {sys.getsizeof(packet)}')
        # print(f'packet_1:       {sys.getsizeof(packet_1)}')
        # print(f'packet_2:       {sys.getsizeof(packet_2)}')
        # print(f'packet_list:    {sys.getsizeof(packet_list)}')
        # print(f'pop:            {sys.getsizeof(pop)}')
        # print(f'rerun:          {sys.getsizeof(rerun)}')
        # print(f'shift_index:    {sys.getsizeof(shift_index)}')
        # print(f'shift_list:     {sys.getsizeof(shift_list)}')
        # print(f'skip:           {sys.getsizeof(skip)}')
        # print('***************************************************************')
    
    # for index, packet in enumerate(packet_list):
    #     if index == 0:
    #         final_packet_xref_list.append(index)
    #         continue
        
    #     for fp_index, ref_index in enumerate(final_packet_xref_list):
    #         ref_packet = packet_list[ref_index]
    #         if packet == ref_packet:
    #             continue
    #         print('***************************************************************')
    #         print(index)
    #         print(packet)
    #         print(ref_packet)
    #         print('***************************************************************')
    #         list_packet = ast.literal_eval(packet)
    #         list_ref_packet = ast.literal_eval(ref_packet)
            
    #         while True:
    #             rerun, list_checkout = compare_inputs(list_packet, list_ref_packet)
                
    #             if not rerun:
    #                 break
            
    #         if list_checkout:
    #             final_packet_xref_list.insert(fp_index, index)
    #             break
    #         del(list_packet)
    #         del(list_ref_packet)
    #     else:
    #         final_packet_xref_list.append(index)
            
    mult_indices = []
    for div_packet in div_packets:
        mult_indices.append(packet_list.index(div_packet) + 1)
        
    print(np.prod(mult_indices))
    # ==========================================================================