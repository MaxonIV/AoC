# -*- coding: utf-8 -*-
"""
    Created on Sat Dec 17 09:26:47 2022
    
    @author: MaxonIV
"""
import os
import glob
import json

dir_path = r'E:\AoC\2022\Day_16'

file_list = glob.glob(os.path.join(dir_path, 'Day_16_Path_Results_*.json'))

report_path = ''
report_minutes = 0
report_flow_rate = 0


gt30_report_path = ''
gt30_report_minutes = 0
gt30_report_flow_rate = 0
gt30_report_flow_rate = 0


for json_file in file_list:
    with open(json_file) as f:
        report = json.load(f)
        
    for key in report.keys():
        if report[key]['minutes'] > 30:
    
            if report[key]['30 minute flow rate'] > gt30_report_flow_rate:
                gt30_report_flow_rate = report[key]['30 minute flow rate']
                
                gt30_report_minutes = report[key]['minutes']
                gt30_report_path = json_file
            continue
        
        if report[key]['flow rate'] > report_flow_rate:
            report_flow_rate = report[key]['flow rate']
            
            report_minutes = report[key]['minutes']
            report_path = json_file
            
print(report_path)
print(report_minutes)
print(report_flow_rate)
print('******')
print(gt30_report_path)
print(gt30_report_minutes)
print(gt30_report_flow_rate)