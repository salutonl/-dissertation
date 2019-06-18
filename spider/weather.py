# -*-coding: UTF-8 -*-
import requests
import pandas as pd
import re

def createCityCode(weather_content):
    data = pd.read_table('/home/pi/dissertation/spider/city_code/city_code.txt', header=None, sep='=')
    data = data.dropna()
    # print(data)
    cityCodeDict = {}
    for code, name in zip(data[0], data[1]):
        cityCodeDict[name] = code
        if name in weather_content:
            print name
            print code
            return code, name

def weather_spider(url, headers):
    response = requests.get(url, headers)
    data = response.content.decode('utf-8')
    weather_pattern = re.compile('<input type="hidden" id="hidden_title" value="(.*?)" />')
    # update_time_pattern = re.compile('<input type="hidden" id="fc_24h_internal_update_time" value="(.*?)"/>')
    detailed_info_pattern = re.compile('<li class="li. hot".*?\n<i></i>.<span>(.*?)</span>\n<em>(.*?)</em>\n<p>(.*?)</p>.*?\n</li>',re.S)

    weather_info = weather_pattern.findall(data)
    # update_time_info = update_time_pattern.findall(data)
    #detailed_info = detailed_info_pattern.findall(data)
    # print(update_time_info)
    # ordered_detailed = []
    #for item in detailed_info:
    #    if item[1] != '减肥指数' and item[1] != '洗车指数' and item[1] != '健臻·血糖指数':
    #        temp = ',' + item[1] + item[0]
    #        ordered_detailed.append(temp)
    all_weather_info = weather_info
    info = ''.join(all_weather_info)
    return info

def get_weather_info(weather_content):
    code, city_name = createCityCode(weather_content)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0.2 Safari/604.4.7'
    }
    #print(city_code)
    url = 'http://www.weather.com.cn/weather1d/%d.shtml' % code
    weather_info = weather_spider(url, headers)
    return weather_info

