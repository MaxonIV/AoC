# -*- coding: utf-8 -*-
"""
    Created on Thu Dec 15 11:38:17 2022
    
    @author: MaxonIV
"""
import numpy as np
    
SB_dic = {
    'bounds': {
        'min_S_x': np.inf,
        'max_S_x': -np.inf,
        'min_S_y': np.inf,
        'max_S_y': -np.inf
    }
}

buffer = 10

with open('Day_15_Input.txt', 'r') as inputs:
    Lines = inputs.readlines()
    
    for index, line_text in enumerate(Lines):
        line = line_text.replace('\n', '')
        
        line_split = line.split(',')
        
        S_x = int(line_split[0].split(' ')[-1].split('=')[-1])
        S_y = int(line_split[1].strip().split(':')[0].split('=')[-1])
        
        B_x = int(line_split[1].split(' ')[-1].split('=')[-1])
        B_y = int(line_split[2].strip().split('=')[-1])
        
        d_x = abs(B_x - S_x)
        d_y = abs(B_y - S_y)
        
        d = d_x + d_y
        
        SB_dic['bounds']['min_S_x'] = min(SB_dic['bounds']['min_S_x'], S_x - (d + buffer))
        SB_dic['bounds']['max_S_x'] = max(SB_dic['bounds']['max_S_x'], S_x + (d + buffer))
        SB_dic['bounds']['min_S_y'] = min(SB_dic['bounds']['min_S_y'], S_y - (d + buffer))
        SB_dic['bounds']['max_S_y'] = max(SB_dic['bounds']['max_S_y'], S_y + (d + buffer))
        
        SB_dic[index + 1] = {
            'S': [S_x, S_y],
            'B': [B_x, B_y],
            'd': d
        }
        
# y = 2000000

# count = 0

# for x in range(SB_dic['bounds']['min_S_x'], SB_dic['bounds']['max_S_x'] + 1):
#     check = False
    
#     for key in SB_dic.keys():
#         if key == 'bounds':
#             continue
         
#         if [x, y] == SB_dic[key]['B']:
#             check = False
#             break
        
#         elif (abs(SB_dic[key]['S'][0] - x) + abs(SB_dic[key]['S'][1] - y)) <= SB_dic[key]['d']:
#             check = True
        
#     if check:
#         count += 1

# print(count)
# y = -1
# beacon_found = False
# freq = 4000000
# while y <= freq and not beacon_found:
#     x = 0
#     y += 1
#     # print(x, y)
#     # y_jump_found = False
    
#     # beacon_found = True
#     # for key in SB_dic.keys():
#     #     if key == 'bounds':
#     #         continue
        
#     #     elif (abs(SB_dic[key]['S'][0] - x) + abs(SB_dic[key]['S'][1] - y)) <= SB_dic[key]['d']:
#     #         beacon_found = False
            
#     #         if SB_dic[key]['S'][1] > y:
#     #             if (y + (SB_dic[key]['S'][1] - y) + (SB_dic[key]['d'] - abs(SB_dic[key]['S'][0] - x)) - 3) < freq:
#     #                 y_jump_found = True
#     #                 y += (SB_dic[key]['S'][1] - y) + (SB_dic[key]['d'] - abs(SB_dic[key]['S'][0] - x)) - 3
#     #         elif (SB_dic[key]['d'] - (abs(SB_dic[key]['S'][0] - x) + abs(y - SB_dic[key]['S'][1])) - 3) > 5:
#     #             if (y + (SB_dic[key]['d'] - (abs(SB_dic[key]['S'][0] - x) + abs(y - SB_dic[key]['S'][1])) - 3)) < freq:
#     #                 y_jump_found = True
#     #                 y += (SB_dic[key]['d'] - (abs(SB_dic[key]['S'][0] - x) + abs(y - SB_dic[key]['S'][1])) - 3)
                
#     #         break
        
#     # if y_jump_found:
#     #     continue
    
#     while x <= freq and not beacon_found:
#         print(x, y)
#         x += 1
        
#         beacon_found = True
#         for key in SB_dic.keys():
#             if key == 'bounds':
#                 continue
            
#             elif (abs(SB_dic[key]['S'][0] - x) + abs(SB_dic[key]['S'][1] - y)) <= SB_dic[key]['d']:
#                 beacon_found = False
                
#                 if SB_dic[key]['S'][0] > x:
#                     if (x + (SB_dic[key]['S'][0] - x) + (SB_dic[key]['d'] - abs(SB_dic[key]['S'][1] - y)) - 3) < freq:
                        
                        
#                         x += (SB_dic[key]['S'][0] - x) + (SB_dic[key]['d'] - abs(SB_dic[key]['S'][1] - y)) - 3
#                 elif (SB_dic[key]['d'] - (abs(SB_dic[key]['S'][1] - y) + abs(x - SB_dic[key]['S'][0])) - 3) > 5:
#                     if (x + (SB_dic[key]['d'] - (abs(SB_dic[key]['S'][1] - y) + abs(x - SB_dic[key]['S'][0])) - 3)) < freq:
#                         x += (SB_dic[key]['d'] - (abs(SB_dic[key]['S'][1] - y) + abs(x - SB_dic[key]['S'][0])) - 3)
                    
#                 break
                
                
# if beacon_found:
#     print(f'Solution: {x}, {y}')
# else:
#     print('WTF')
    
# ==============================================================================
def check_point(SB_dic, x, y, s_key):
    check = True
    
    for key in SB_dic.keys():
        if key == 'bounds' or key == s_key:
            continue
        
        elif (abs(SB_dic[key]['S'][0] - x) + abs(SB_dic[key]['S'][1] - y)) <= SB_dic[key]['d']:
            check = False
    
    return check
# ==============================================================================
freq = 4000000
check = False
for key in SB_dic.keys():
    if key == 'bounds':
        continue
    
    print(key)

    x_0 = SB_dic[key]['S'][0]
    y_0 = SB_dic[key]['S'][1]
    
    d = SB_dic[key]['d']
    
    d_x = 0
    d_y = d
    
    # ==============
    while d_y >= 0 and not check:
        x = x_0 + d_x
        y = y_0 + d_y + 1
        
        if x >= 0 and y >= 0 and x <= freq and y <= freq:
            check = check_point(SB_dic, x, y, key)
            
            if check:
                break
        
        d_x += 1
        d_y -= 1
    # ==============
    d_x = d
    d_y = 0

    while d_x >= 0 and not check:
        x = x_0 + d_x + 1
        y = y_0 - d_y
        
        if x >= 0 and y >= 0 and x <= freq and y <= freq:
            check = check_point(SB_dic, x, y, key)
            
            if check:
                break
        
        d_x -= 1
        d_y += 1
    # ==============
    d_x = 0
    d_y = d
    
    while d_y >=0 and not check:
        x = x_0 - d_x
        y = y_0 - d_y - 1
        
        if x >= 0 and y >= 0 and x <= freq and y <= freq:
            check = check_point(SB_dic, x, y, key)
            
            if check:
                break
        
        d_x += 1
        d_y -= 1
    # ==============
    d_x = d
    d_y = 0

    while d_x >= 0 and not check:
        x = x_0 - d_x - 1
        y = y_0 + d_y
        
        if x >= 0 and y >= 0 and x <= freq and y <= freq:
            check = check_point(SB_dic, x, y, key)
            
            if check:
                break
        
        d_x -= 1
        d_y += 1
        
    if check:
        break

print(x, y)
print(freq*x + y)
                
                



































