#-*- coding: utf-8 -*-
from unittest import case
import io
import sys
from bs4 import BeautifulSoup
from matplotlib.style import available
from selenium import webdriver
import datetime
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime

 
def daysData():
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

    driver = webdriver.Chrome()


    url = "https://www.cwb.gov.tw/V8/C/W/Town/Town.html?TID=1001801"
    driver.get(url)
    open('test.html','wb').write(driver.page_source.encode('utf-8'))
    l=driver.find_element_by_id("Tab_weeksTable")
    l.click()
    # continue
    soup = BeautifulSoup(driver.page_source, features='lxml')

    d = []
    d = {'PC7_Wx':[],'PC7_MaxT':[],'PC7_MinT':[],'PC7_Po':[],'PC7_MaxAT':[],'PC7_MinAT':[],'PC7_RH':[],'PC7_BF':[]}
    counter=0 
    
    for id,list in d.items():
        if counter ==0:
            
            test = soup.find('th', { 'id' : id })
            test = test.findPrevious('tr')
            test = test.find_all('td')
            l  = []
            for td in test:
                l.append(td.findNext('img').get('title'))
            d[id] = l

            
        elif  counter ==6 or counter ==7 or counter==3:
            test = soup.find('th', { 'id' : id })
            test = test.findPrevious('tr')
            test = test.find_all('td')
            l  = []
            for td in test:
                l.append(td.text)
            d[id] = l
        else:
            test = soup.find('th', { 'id' : id })
            test = test.findPrevious('tr')
            test = test.find_all('td')
            l  = []
            for td in test:
                l.append(td.findNext('span').text)
            d[id] = l
        counter+=1
    # print(d)

    d["PC7_T"] = [0 for i in range(14)]
    for i in range(14):
        d["PC7_T"][i]=(int(d['PC7_MaxT'][i])+int(d['PC7_MinT'][i]))/2

    d["PC7_AT"] = [0 for i in range(14)]
    for i in range(14):
        d["PC7_AT"][i]=(int(d['PC7_MaxAT'][i])+int(d['PC7_MinAT'][i]))/2
    res = {i:{} for i in range(1,15)}
    counter =1 
    for k,v in d.items():
        counter=1
        for i in v:
            res[counter][k]=i
            counter +=1

    # print(res)
    driver.quit() 
    return res

def findDay(day):
    res={}
    dd = daysData()[day]
    res['datetime'] = str(datetime.datetime.now()).split(".")[0]
    Y = 2000 # dummy leap year to allow input X-02-29 (leap day)
    seasons = [(1, (datetime.date(Y,  1,  1),  datetime.date(Y,  3, 20))),
            (2, (datetime.date(Y,  3, 21),  datetime.date(Y,  6, 20))),
            (3, (datetime.date(Y,  6, 21),  datetime.date(Y,  9, 22))),
            (4, (datetime.date(Y,  9, 23),  datetime.date(Y, 12, 20))),
            (1, (datetime.date(Y, 12, 21),  datetime.date(Y, 12, 31)))]

    def get_season(now):
        if isinstance(now, datetime.datetime):
            now = now.date()
        now = now.replace(year=Y)
        return next(season for season, (start, end) in seasons
                    if start <= now <= end)

    
    res['season'] = get_season(datetime.date.today())
    res['holiday'] = 0
    res['workingday'] = 1
    
        
        
    res['weather'] = 3 if dd['PC7_Wx'][len(dd['PC7_Wx'])-1]=='雨' else 1
    res['temp'] = dd['PC7_T']
    res['atemp'] = dd['PC7_AT']
    res['humidity'] = dd['PC7_RH'][0:len(dd['PC7_RH'])-1]
    wl = [0 for i in range(6)]
    counter=2
    wl[0] = 0
    for i in range(1,6):
        wl[i] = wl[i-1]+counter
        counter+=2

    res['windspeed'] = (wl[int(dd['PC7_BF'])]+wl[int(dd['PC7_BF'])-1])/2
    return res
if __name__=='__main__':
    day=findDay(1)
    print(day)





