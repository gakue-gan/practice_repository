#!/usr/bin/env python
# coding: utf-8

# In[193]:


import pandas as pd
import numpy
import glob
from selenium import webdriver
import time 
import os
import datetime
from bs4 import BeautifulSoup
import urllib.request as req
import pprint
import re
import json
from lxml import html
import requests


# In[194]:


#ページアクセス
browser = webdriver.Chrome(executable_path = 'C:\\Users\\ok37g\\OneDrive\\デスクトップ\\MyScraving\\chromedriver.exe')
browser.implicitly_wait(1)
url = 'https://www.fe-siken.com/fehani.html'
browser.get(url)
time.sleep(1)


# In[195]:


#ページ情報取得
response = req.urlopen(url)
parse_html = BeautifulSoup(response, 'html.parser')
lxml_converted_html = html.fromstring(str(parse_html))
print(url + 'の情報を取得しました')


# In[196]:


large_genre_list = []
repeat_num = [14, 4, 8]
for i in range(1,4):
    large_genre = lxml_converted_html.xpath('//*[@id="sideCol"]/div/ul[5]/li['+str(i)+']/a')[0].text
    middle_genre_list = []
    
    for j in range(1,repeat_num[i-1]):
        middle_genre = lxml_converted_html.xpath('//*[@id="mainCol"]/div[2]/div[' + str(i + 2)+ ']/dl/dt['+ str(j) +']')[0].text.split('．')
        small_genre_integrated = lxml_converted_html.xpath('//*[@id="mainCol"]/div[2]/div[' + str(i + 2) + ']/dl/dd[' + str(j) + ']')[0].text
        small_genre = re.split('[()・]', small_genre_integrated)
        
        small_genre_list = []
        for k in range(1,len(small_genre)-1):
            small_genre_dict = {
            'small_genre_id':k,
            'small_genre_name':small_genre[k],
            }
            small_genre_list.append(small_genre_dict)
    
        middle_genre_dict = {
            'middle_genre_id':middle_genre[0],
            'middle_genre_name':middle_genre[1],
            'small_genre':small_genre_list
        }
        middle_genre_list.append(middle_genre_dict)
    
    large_dict = {
        'large_genre_id':i,
        'large_genre_name':large_genre,
        'middle_genre':middle_genre_list
    }
    large_genre_list.append(large_dict)
pprint.pprint(large_genre_list)


# In[199]:


export_url = 'C:\\Users\\ok37g\\OneDrive\\デスクトップ\\MyScraving\\jenre.json'

with open(export_url, 'w') as f:
    json.dump(large_genre_list, f, ensure_ascii=False, indent=4)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




