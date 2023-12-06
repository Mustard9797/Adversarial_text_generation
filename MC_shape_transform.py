import requests
import re
import urllib.request
from bs4 import BeautifulSoup
from collections import deque
from html.parser import HTMLParser
from urllib.parse import urlparse
import os
import pathlib
import openai
import configparser
import pandas as pd
import tiktoken
import numpy as np
import datetime
import random
from ast import literal_eval
from openai.embeddings_utils import distances_from_embeddings, cosine_similarity

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
    config.read("D:\\itri\\config.ini",encoding="utf-8")

    dir = config['adversarial']['dir']
    os.chdir(dir)
    openai.api_key = config['api']['key']

    #整理好的csv檔預設先放在processed資料夾裡
    if os.path.isdir('processed'):
        pass
    else:
        print("processed dir does not exist")
        os.makedirs('processed')

    df = pd.read_csv('形近同音近音字.csv',encoding="utf_8_sig")
    max = len(df)

    #欲轉換的文檔，需為帶有index和'context'欄位的dataframe
    file = config['multiple_choice']['dir'] + '\\processed\\scraped.csv'

    context_df = pd.read_csv( file,encoding="utf_8_sig",index_col=0)
    context_df['transform context'] = ""

    for l in range(len(context_df)):
        outcome = ""
        for text in context_df.loc[l,'context']:
            outcome += shape_transform(df,text,max)
        print(outcome)
        context_df.loc[l,'transform context'] = outcome
    timestamp = datetime.datetime.now().strftime('%Y_%b%d_%H%M%S')
    context_df.to_csv('processed\\' + timestamp + '_shape_transform.csv',encoding="utf_8_sig")

    print("Shape transform end")