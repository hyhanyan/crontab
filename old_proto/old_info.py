#coding:utf-8

import string
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

def process(line,dict):
    pid = line[1].strip().split(':')[1].strip()
    name = line[0].strip().split(':')[1].strip()
    if dict.has_key(pid):
        dict[pid] = dict[pid] + ";" + name
    else:
        dict[pid] = name

def process_ts(lines,dict):
    pid = ''
    tmp_lines = ''
    for line in lines:
        if line.startswith('#'):
            continue
        if line.startswith('PRODUCT_ID'):
            pid = line.strip().split(':')[1].strip()
        tmp_lines = tmp_lines + ';' + line.strip()
    
    tmp_lines = tmp_lines[1:]
    if pid and dict.has_key(pid):
        dict[pid] = dict[pid] + ";|" + str(tmp_lines)
    else:
        dict[pid] = str(tmp_lines)

def ReadFile_App(filename,dict_app_list):
    fp = open(filename,'r')
    try:
        lines = fp.readlines()
    finally:
        fp.close()

    for (num,line) in enumerate(lines):
        if line.startswith('#'):
            continue
        if line.startswith('[@'):
            text_line = lines[num+1:num+5]
            process(text_line,dict_app_list);
    
    fp.close()

def ReadFile_Ts(filename,dict_ts_product):
    fp = open(filename,'r')
    try:
        lines = fp.readlines()
    finally:
        fp.close()

    start = 0
    status = 1
    num = 0
    for (num,line) in enumerate(lines):
        if line.startswith('#'):
            continue
        if line.startswith('[@') and status == 1:
            start = num
            status += 1
        elif line == '\n' and status == 2:
            text_line = lines[start+1:num]
            process_ts(text_line,dict_ts_product);
            status = 1
            start = 0
    
    if start != 0 and status == 2:
        text_line = lines[start+1:num]
        process_ts(text_line,dict_ts_product);

    fp.close()

def Select_desc(dict_old_description):
    fp = open("sql/result.txt", 'r')
    try:
        lines = fp.readlines()
    finally:
        fp.close()
    
    for (num,line) in enumerate(lines):
        if num == 0:
            continue
        old_list = line.strip().split()
        pid = old_list[0]
        if len(old_list) == 2:
            desc = old_list[1]
        else:
            desc = ''
        dict_old_description[pid] = desc 

def InsertMysql(dict_app_list,dict_ts_product,dict_old_description):
    fp = open("sql/app_old_info.sql",'w')

    for (pid,conf) in dict_ts_product.items():
        if not pid:
            continue
        if dict_old_description.has_key(pid):
            if dict_app_list.has_key(pid):
                sql = "replace into app_old_info(pid,name,description,conf) values(" + pid + ",'" + dict_app_list[pid] + "','"  + dict_old_description[pid] + "','" + conf + "');"
            else:
                sql = "replace into app_old_info(pid,description,conf) values(" + pid + ",'" + dict_old_description[pid] + "','" + conf + "');"
        else:
            if dict_app_list.has_key(pid):
                sql = "replace into app_old_info(pid,name,conf) values(" + pid + ",'" + dict_app_list[pid] + "','" + conf + "');"
            else:
                sql = "replace into app_old_info(pid,conf) values(" + pid + ",'" + conf + "');"
            

        fp.write(sql + '\n')

    fp.close()    
        
if __name__ == '__main__':
    dict_app_list ={}
    dict_ts_product={}
    dict_old_description = {}
    filename = "conf/ll.conf"
    filename_ts = "conf/lx.conf"


    ReadFile_App(filename,dict_app_list)
    ReadFile_Ts(filename_ts,dict_ts_product)
    Select_desc(dict_old_description)
    InsertMysql(dict_app_list,dict_ts_product,dict_old_description)
    



