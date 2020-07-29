#!/usr/bin/env python
# coding: utf-8

# In[45]:


import openpyxl
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


# In[46]:


browser = webdriver.Chrome(executable_path = 'C:\\Users\\ok37g\\OneDrive\\デスクトップ\\MyScraving\\chromedriver.exe')
browser.implicitly_wait(1)


# In[47]:


#ページアクセス
URL='https://www.fe-siken.com'
for_login='/fekakomon.php'
browser.get(URL + for_login)
time.sleep(2)
print('基本情報トップページ表示')


# In[48]:


#トップページ情報取得
response = req.urlopen(URL + for_login)
parse_html = BeautifulSoup(response, 'html.parser')
print(URL + for_login + 'の情報を取得しました')


# In[76]:


#試験URLの取得
def convert_era(ja_year):
    if '令和元' == ja_year:
        east_year = 2019
        return east_year
    if '令和' in ja_year:
        east_year = int(ja_year.split('和')[1]) + 2018
    east_year = int(ja_year) + 1988

    return east_year

tmp = parse_html.select('ul#testMenu > li')[0]
menu_lists = tmp.find_all('a')
test_lists = []

for li in menu_lists:
    title = li.text
    url = URL + li.attrs['href']
    info = re.split('[成和年]', title)
    ja_year = info[1]
    season = info[2]
    if '令和'in title:
        ja_year = '令和' + ja_year
    year = convert_era(ja_year)
    
    isSpring = True
    if season == '秋期':
        isSpring = False
    
   
    
    test_info = {
        'title':title,
        'url':url,
        'year':year,
        'isSpring':isSpring,
    }
    test_lists.append(test_info)

tmp = parse_html.select('ul#testMenu2 > li')
menu2_lists = tmp[0].find_all('a')
for li in menu2_lists:
    title = li.text
    url = URL + li.attrs['href']
    info = re.split('年', title)
    year = info[0] + '年'
    season = info[1]
    
    isSpring = True
    if season == '秋期':
        isSpring = False
    
    info = {
        'title':title,
        'url':url,
        'year':year,
        'isSpring':isSpring,
    }
    test_lists.append(info)
print('試験URLを取得しました')
test_lists


# In[77]:


#問題の論点取得
current_url = test_lists[0]['url']
year = test_lists[0]['year']
isSpring = test_lists[0]['isSpring']

questions_list = []
table = pd.read_html(current_url, header = 0)[1]

table_dict = table.to_dict(orient = 'index')
for index, row in table_dict.items():
    if index == 0 or index == 51 or index == 62:
        continue
    question_id = index
    if 51 < index < 62:
        question_id += 1
    elif 62 < index:
        question_id += 2
    point= row['論点']
    
    question_info = {
        'question_id':question_id,
        'point':point,
        'year':year,
        'isSpring':isSpring
    }
    questions_list.append(question_info)
    
print('論点を取得しました。')
questions_list


# In[78]:


#問題・解答・ジャンルを取得しました。
qnumber = questions_list[0]['question_id']
browser.get(current_url + 'q' + str(qnumber) + '.html')
question_statement = browser.find_element_by_xpath('//*[@id="mainCol"]/div[2]/div[2]').text
choice_1 = browser.find_element_by_id('select_a').text
choice_2 = browser.find_element_by_id('select_i').text
choice_3 = browser.find_element_by_id('select_u').text
choice_4 = browser.find_element_by_id('select_e').text
answer_tmp = browser.find_element_by_id('answerChar').text
answer = 1
if answer_tmp == 'イ':
    answer = 2
elif answer_tmp == 'ウ':
    answer = 3
elif answer_tmp == 'エ':
    answer = 4
genre_info = browser.find_element_by_xpath('//*[@id="mainCol"]/div[2]/p').text.split(' » ')
large_genre = genre_info[0]
middle_genre = genre_info[1]
small_genre = genre_info[2]

explanation = browser.find_element_by_xpath('//*[@id="mainCol"]/div[2]/div[6]').text
questions_list[0]['large_genre_id']=large_genre
questions_list[0]['middle_genre_id']=middle_genre
questions_list[0]['small_genre_id']=small_genre
questions_list[0]['question_statement']=question_statement
questions_list[0]['choice_1']=choice_1
questions_list[0]['choice_2']=choice_2
questions_list[0]['choice_3']=choice_3
questions_list[0]['choice_4']=choice_4
questions_list[0]['answer']=answer
questions_list[0]['explanation']=explanation

questions_list[0]


# In[88]:


year = str(test_lists[0]['year'])
season = 'autumn'
if test_lists[0]['isSpring']:
    season = 'spring'
export_url = 'C:\\Users\\ok37g\\OneDrive\\デスクトップ\\MyScraving\\' + year + season + '.json'
    
with open(export_url, 'w') as f:
    json.dump(questions_list, f, ensure_ascii=False,indent=4)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




