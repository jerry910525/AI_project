# -*- coding: utf-8 -*-
from unittest import case
from bs4 import BeautifulSoup
from matplotlib.style import available
from selenium import webdriver
import datetime
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup

date = []
region = []
station = []
available_borrow_value = []
available_stop_value = []
temp = []
rain = []
count = 2
r=0

driver = webdriver.Chrome()

while 1:
    if r>count:
        break
    url = "https://www.youbike.com.tw/region/main/stations/"
    driver.get(url)
    open('test.html','wb').write(driver.page_source.encode('utf-8'))
    # continue
    soup = BeautifulSoup(driver.page_source, features='lxml')
    tbody = soup.find('tbody',{'id':'setarealist'})
    trs = tbody.find_all('tr')
    for tr in trs:
        date.append(str(datetime.datetime.now()))
        t=0
        for td in tr.find_all("td"):
            if t==0:
                region.append(td.text)
            if t==1:
                station.append(td.text)
            if t==2:
                available_borrow_value.append(td.text)
            if t==3:
                available_stop_value.append(td.text)
            t+=1
    url = "https://www.cwb.gov.tw/V8/C/W/Town/Town.html?TID=1001801"
    driver.get(url)
    # open('test.html','wb').write(driver.page_source.encode('utf-8'))
    
    soup = BeautifulSoup(driver.page_source, features='lxml')
    tbody = soup.find('table',{'class':"table cubeV9-table pc"})
    # print(tbody)
    tds= tbody.find_all("td")
    
    t = 0 
    for td in tds:
        if t==8:
            temp.append(td.text[0:2])
        if t==11:  
            rain.append(td.text)
        t=t+1
    time.sleep(6)
    r+=1
    temp.extend([temp[len(temp)-1] for i in range(len(date)-len(temp))])
    rain.extend([rain[len(rain)-1] for i in range(len(date)-len(rain))])
driver.quit() 

table = {
"時間":date,
"區域":region,
"租賃站點查詢":station,
"可借車輛":available_borrow_value,
"可停空位":available_stop_value,
"溫度":temp,
"時雨量":rain
}



df = pd.DataFrame(table)
df = df.reset_index(drop=True)    
df.to_csv(( 'result.csv'), encoding = 'utf-8')


