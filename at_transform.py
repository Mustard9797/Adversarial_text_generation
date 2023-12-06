import os
import pathlib
import configparser
import pandas as pd
import numpy as np
import datetime
import random
from ast import literal_eval

#透過遍歷字典的方式查找，若存在於字典，則轉換成同音國字
def pronounce_transform(df,text,max):
    for i in range(max):
        if df.loc[i,'國字'] == text:
            try:
                replace_list = df.loc[i,'同音國字'].split(';')
                replace_word = random.choice(replace_list)
                return replace_word
            except:
                continue
    return text

#透過遍歷字典的方式查找，若存在於字典，則轉換成型近字
def shape_transform(df,text,max):
    for i in range(max):
        if df.loc[i,'國字'] == text:
            try:
                replace_list = df.loc[i,'型近字'].split(';')
                replace_word = random.choice(replace_list)
                return replace_word
            except:
                continue
    return text


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read("/home/mcas/liao/chatgpt_evaluation/adversarial_text/config.ini",encoding="utf-8")

    dir = config['adversarial']['dir']
    os.chdir(dir)

    #若seed有設定，固定seed
    if bool(config['test']['open_seed']):
        random.seed(int(config['test']['seed']))

    #設定轉換的比例，需介於0~1之間
    trans_proportion = float(config['test']['proportion'])

    #整理好的csv檔預設先放在processed資料夾裡
    if os.path.isdir('processed'):
        pass
    else:
        print("processed dir does not exist")
        os.makedirs('processed')

    df = pd.read_csv('形近同音近音字.csv',encoding="utf_8_sig")
    max = len(df)
    
    option = input("1.Pronounce 2.Shape: ")

    if option == "1":
        #一字多音對照表，將破音字從轉換列表中排除
        ignore_df = pd.read_csv('proccessed_國語一字多音審訂表2012.csv',encoding="utf_8_sig")
        ignore_list = ignore_df['國字'].tolist()

        #欲轉換的文檔
        file = os.path.join(config['adversarial']['dir'],'negative.csv')

        context_df = pd.read_csv( file ,encoding="utf_8_sig")
        context_df['transform context'] = ""
        
        for l in range(len(context_df)):
            outcome = ""
            text = context_df.loc[l,'context']
            test_list = random.sample(text,int(len(text)*trans_proportion))
            for t in text:
                if t not in test_list:
                    outcome += t
                elif t in ignore_list:
                    outcome += t
                else:
                    outcome += pronounce_transform(df,t,max)
            print(outcome)
            context_df.loc[l,'transform context'] = outcome
        timestamp = datetime.datetime.now().strftime('%Y_%b%d_%H%M%S')
        context_df.to_csv('processed' + os.sep + timestamp + '_pronnounce_transform.csv',encoding="utf_8_sig")

        print("Pronnounce transform end")
    elif option == "2":
        #忽略名單，待整理
        ignore_list = []

        #欲轉換的文檔
        file = os.path.join(config['adversarial']['dir'],'negative.csv')

        context_df = pd.read_csv( file ,encoding="utf_8_sig")
        context_df['transform context'] = ""
        
        for l in range(len(context_df)):
            outcome = ""
            text = context_df.loc[l,'context']
            test_list = random.sample(text,int(len(text)*trans_proportion))
            for t in text:
                if t not in test_list:
                    outcome += t
                elif t in ignore_list:
                    outcome += t
                else:
                    outcome += shape_transform(df,t,max)
            print(outcome)
            context_df.loc[l,'transform context'] = outcome
        timestamp = datetime.datetime.now().strftime('%Y_%b%d_%H%M%S')
        context_df.to_csv('processed' + os.sep + timestamp + '_shape_transform.csv',encoding="utf_8_sig")

        print("Shape transform end")
    else:
        print("Wrong option!")