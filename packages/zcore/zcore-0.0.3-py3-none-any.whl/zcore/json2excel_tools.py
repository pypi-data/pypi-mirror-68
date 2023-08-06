# encoding=utf-8
import json
import os
import pandas as pd
from collections import defaultdict

from core.file_tools import read_txtline_by_matchpath
def json2excel(datas,excel_path):
    if type(datas) != "list":
        Exception("data 必须是list类型")
    df = pd.DataFrame([datas])
    with pd.ExcelWriter(excel_path) as f:
        df.to_excel(f, sheet_name='all')
    pass
def json_complex_2excel(datas,excel_path):
    if type(datas) != "list":
        Exception("data 必须是list类型")
    slave_dic={"feifei":[{"id":"1","name":"feifei"}]}
    main_list = []

    for data in datas:
        c_dic = {}
        for n, v in data.items():
            # print(type(v))
            # print(type(v) == 'list')
            # print(n, '====', v, '===', type(v))
            if isinstance(v,list):
                print(n, '====', v, '===', type(v))
                if n in slave_dic:
                    for d_item in v:
                        slave_dic[n].append(d_item)
                else:
                    slave_dic[n]=v
            else:
                c_dic[n] = v

        main_list.append(c_dic)


    df = pd.DataFrame(main_list)
    print('slave_dic','***'*50)
    print(slave_dic)
    with pd.ExcelWriter(excel_path) as f:
        df.to_excel(f, sheet_name='main')
        for ik in slave_dic.keys():
            ilist = slave_dic[ik]
            df2 = pd.DataFrame(ilist)
            df2.to_excel(f, sheet_name=ik)

def json_complex_2excel_fk(datas,excel_path,main_col):
    if type(datas) != "list":
        Exception("data 必须是list类型")
    slave_dic={"feifei":[{"id":"1","name":"feifei"}]}
    main_list = []

    for data in datas:
        c_dic = {}
        for n, v in data.items():
            # print(type(v))
            # print(type(v) == 'list')
            # print(n, '====', v, '===', type(v))
            if isinstance(v,list):
                print(n, '====', v, '===', type(v))
                if n in slave_dic:
                   pass
                else:
                    slave_dic[n]=[]

                for d_item in v:
                    d_item[main_col] = data.get(main_col)
                    slave_dic[n].append(d_item)
                #
            else:
                c_dic[n] = v

        main_list.append(c_dic)


    df = pd.DataFrame(main_list)
    print('slave_dic','***'*50)
    print(slave_dic)
    with pd.ExcelWriter(excel_path) as f:
        df.to_excel(f, sheet_name='main')
        for ik in slave_dic.keys():
            ilist = slave_dic[ik]
            df2 = pd.DataFrame(ilist)
            df2.to_excel(f, sheet_name=ik)


if __name__ == "main":
    pass
    input_path = r'c:\test\**\jsonBasic.json'
    total_list=[]
    for line in read_txtline_by_matchpath(input_path):
        obj = json.loads(line)
        if(obj['status'] != 0):
            continue
        total_list.append(obj['data'])
    json_complex_2excel_fk(total_list,'feifei.xlsx','entName')
