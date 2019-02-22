#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @File    : getWeather.py
# @Author  : Findyou
# @email   : albert.peng@foxmail.com
# @Python  : 3.6
# @Software: PyCharm

__author__ = "Findyou"
__version__ = "0.1"
__date__ = "2017/7/4 23:27"

import requests
import csv
import random
import time
import socket
import http.client
import datetime
import os
from bs4 import BeautifulSoup

'''
1.模拟网页请求
'''
def get_content(cityCode , data = None):
    url = 'http://www.weather.com.cn/weather/'+cityCode+'.shtml'
    header={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.235'
    }
    timeout = random.choice(range(80, 180))
    while True:
        try:
            rep = requests.get(url,headers = header,timeout = timeout)
            rep.encoding = 'utf-8'
            # req = urllib.request.Request(url, data, header)
            # response = urllib.request.urlopen(req, timeout=timeout)
            # html1 = response.read().decode('UTF-8', errors='ignore')
            # response.close()
            break
        # except urllib.request.HTTPError as e:
        #         print( '1:', e)
        #         time.sleep(random.choice(range(5, 10)))
        #
        # except urllib.request.URLError as e:
        #     print( '2:', e)
        #     time.sleep(random.choice(range(5, 10)))
        except socket.timeout as e:
            print( '3:', e)
            time.sleep(random.choice(range(8,15)))

        except socket.error as e:
            print( '4:', e)
            time.sleep(random.choice(range(20, 60)))

        except http.client.BadStatusLine as e:
            print( '5:', e)
            time.sleep(random.choice(range(30, 80)))

        except http.client.IncompleteRead as e:
            print( '6:', e)
            time.sleep(random.choice(range(5, 15)))

    return rep.text

'''
timeout是设定的一个超时时间，取随机数是因为防止被网站认定为网络爬虫。
然后通过requests.get方法获取网页的源代码、
rep.encoding = ‘utf-8’是将源代码的编码格式改为utf-8（不该源代码中中文部分会为乱码）
下面是一些异常处理
返回 rep.text
'''

'''
1.解析提取数据
'''
def get_data(html_text,cityCode):
    final = []
    bs = BeautifulSoup(html_text, "html.parser")  # 创建BeautifulSoup对象
    body = bs.body # 获取body部分
    data = body.find('div', {'id': '7d'})  # 找到id为7d的div
    ul = data.find('ul')  # 获取ul部分
    li = ul.find_all('li')  # 获取所有的li
    today=datetime.datetime.now()   # 获得当天日期
    # 获得 日:7天的日期
    dayList={today.strftime('%d') : today.strftime('%Y-%m-%d'),
             (today + datetime.timedelta(days=1)).strftime('%d'):(today + datetime.timedelta(days=1)).strftime('%Y-%m-%d'),
             (today + datetime.timedelta(days=2)).strftime('%d'):(today + datetime.timedelta(days=2)).strftime('%Y-%m-%d'),
             (today + datetime.timedelta(days=3)).strftime('%d'):(today + datetime.timedelta(days=3)).strftime('%Y-%m-%d'),
             (today + datetime.timedelta(days=4)).strftime('%d'):(today + datetime.timedelta(days=4)).strftime('%Y-%m-%d'),
             (today + datetime.timedelta(days=5)).strftime('%d'):(today + datetime.timedelta(days=5)).strftime('%Y-%m-%d'),
             (today + datetime.timedelta(days=6)).strftime('%d'):(today + datetime.timedelta(days=6)).strftime('%Y-%m-%d'),
             }

    for day in li: # 对每个li标签中的内容进行遍历
        temp = []
        temp.append(cityCode) #添加城市
        date = day.find('h1').string  # 找到日期
        #temp.append(date)  # 添加到temp中
        date_num=date.replace('）','').split('（')[0]   # 5日（明天） ，替换）为空，以（为分隔符切片，5日
        tmp_num=date_num.replace('日','')    # 获得日的数字
        for d in dayList.keys():
            if int(d) == int(tmp_num) :
                # 对比daylist中的日与爬虫中的日是否同相等
                date_num=dayList[d]

        temp.append(date_num)  # 添加到temp中
        # date_cn = date.replace('）', '').split('（')[1]  # 5日（明天） ，替换）为空，以（为分隔符切片，明天，
        # temp.append(date_cn)  # 添加到temp中

        inf = day.find_all('p')  # 找到li中的所有p标签
        temp.append(inf[0].string,)  # 第一个p标签中的内容（天气状况）加到temp中
        if inf[1].find('span') is None:
            temperature_highest = None # 天气预报可能没有当天的最高气温（到了傍晚，就是这样），需要加个判断语句,来输出最低气温
        else:
            temperature_highest = inf[1].find('span').string  # 找到最高温
            temperature_highest = temperature_highest.replace('℃', '')  # 到了晚上网站会变，最高温度后面也有个℃
        temperature_lowest = inf[1].find('i').string  # 找到最低温
        temperature_lowest = temperature_lowest.replace('℃', '')  # 最低温度后面有个℃，去掉这个符号
        temp.append(temperature_highest)   # 将最高温添加到temp中
        temp.append(temperature_lowest)   #将最低温添加到temp中
        final.append(temp)   #将temp加到final中
    #print(final)
    return final

def write_add_data(data, name):
    file_name = name
    with open(file_name, 'a', errors='ignore', newline='',encoding='utf-8') as f:
            f_csv = csv.writer(f)
            f_csv.writerows(data)

def write_new_data(data, name):
    file_name = name
    with open(file_name, 'w', errors='ignore', newline='',encoding='utf-8') as f:
            f_csv = csv.writer(f)
            f_csv.writerows(data)

def read_cityCode(city):
    city=city
    with open("cityCode.csv", 'r', errors='ignore',encoding='utf-8') as f:
        for line in f.readlines():
            if city == line.strip().split(',')[1] :
                cityCode=line.strip().split(',')[0]
    return cityCode

def get_weather(city):
    cityCode = read_cityCode(city)
    weather = []
    day = datetime.datetime.now().strftime('%Y-%m-%d')  # 今天日期
    weather_file=day+"weather.csv"

    # 文件如果已存在数据则从文件中获取，现只每天爬取一次数据，后面再做更新机制
    if os.path.exists(weather_file):
        with open(weather_file, 'r', errors='ignore',encoding='utf-8') as f:
            for line in f.readlines():
                if cityCode == line.strip().split(',')[0] :
                    weather.append(line.strip().split(','))

    #  如果weather为空，则从网上爬取数据并保存
    if len(weather) == 0:
        html = get_content(cityCode)  # 城市码
        print("网上爬取天气数据")
        result = get_data(html, cityCode)
        write_add_data(result,weather_file)
        weather=result


    chat="未查到天气数据，请确认是否输入有误"
    for k in weather :
        if day == k[1]:
            if k[3] is None:
                chat="今天"+city+"天气," + k[2] + ",温度" + k[4]
            else:
                chat="今天"+city+"天气," + k[2] + ",温度" + k[3] + "到" + k[4]

    return chat

if __name__ == '__main__':
    city="深圳"
    weather=get_weather(city)  # 获得七天天气
    print(weather)
