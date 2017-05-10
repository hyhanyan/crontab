#coding=utf-8

import string, sys
import json
#import MySQLdb

def process(line,dict,dict_desc):
    pid = line[0].strip().split(':')[1].strip()
    key = line[1].strip().split(':')[1].strip()
    desc = line[2].strip().split(':')[1].strip()
    if dict.has_key(pid):
        dict[pid] = dict[pid] + ";" + key
    else:
        dict[pid] = key
    if dict_desc.has_key(pid):
        dict_desc[pid] = dict_desc[pid] + ";" + desc
    else:
        dict_desc[pid] = desc

def ReadFile_App(filename,dict_app_list_key,dict_app_list_desc):
    fp = open(filename,'r')
    try:
        lines = fp.readlines()
    finally:
        fp.close()

    for (num,line) in enumerate(lines):
        if line.startswith('#'):
            continue
        if line.startswith('[@'):
            text_line = lines[num+1:num+4]
            process(text_line,dict_app_list_key,dict_app_list_desc);

    fp.close()

def ReadFile_Ts(filename,dict):
    fresult = filename + ".result"
    
    fp = open(filename,'r')
    try:
        lines = fp.readlines()
    finally:
        fp.close()
   
    fw = open(fresult,'w')

    for line in lines:
        if line.startswith('#'):
            continue
        fw.write(line)
    fp.close()
    fw.close()

    f = file(fresult)
    data = json.load(f)

    for (index,value) in enumerate(data):
        pid = value['product_id']
        if dict.has_key(pid):
            dict[pid] = dict[pid] + ";" + json.dumps(value)
        else:
            dict[pid] = json.dumps(value)[1:-1]

def InsertMysql(dict_app_list_key,dict_app_list_desc,dict_ts_product):
    fp = open("sql/app_new_info.sql",'w')

    for (pid,conf) in dict_ts_product.items():
        if not pid:
            continue
        pid = str(pid)
        if dict_app_list_desc.has_key(pid):
            if dict_app_list_key.has_key(pid):
                sql = "replace into app_info_v2(pid,key_new,description,conf) values(" + pid + ",'" + dict_app_list_key[pid] + "','"  + dict_app_list_desc[pid] + "','" + conf + "');"
            else:
                sql = "replace into app_info_v2(pid,description,conf) values(" + pid + ",'" + dict_app_list_desc[pid] + "','" + conf + "');"
        else:
            if dict_app_list_key.has_key(pid):
                sql = "replace into app_info_v2(pid,key_new,conf) values(" + pid + ",'" + dict_app_list_key[pid] + "','" + conf + "');"
            else:
                sql = "replace into app_info_v2(pid,conf) values(" + pid + ",'" + conf + "');"
            

        fp.write(sql + '\n')

    fp.close()   

if __name__ == '__main__':
    dict_app_list_key ={}
    dict_app_list_desc ={}
    dict_ts_product={}
    filename = "conf/ll.conf"
    filename_ts = "conf/lx.conf"

    ReadFile_Ts(filename_ts,dict_ts_product)
    ReadFile_App(filename,dict_app_list_key,dict_app_list_desc)
    InsertMysql(dict_app_list_key,dict_app_list_desc,dict_ts_product) 




