#!/usr/bin/env python

import sys
import xml.etree.ElementTree as ET
import requests

def downloadYandexFc():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    }
    r = requests.get('https://export.yandex.ru/bar/reginfo.xml?region=193', headers=headers)
    return r.text

def formatForecastYandex( forecast ):
    wind_speed = forecast.find('wind_speed').text
    temperature = forecast.find('temperature').text
    return 'YA:t%s%sC %sm/c' % (temperature, chr(0xF8), wind_speed)

def parseYandex ( data ):
#    tree = ET.parse('yandex.xml')
#    root = tree.getroot()
    info = ET.fromstring(data)
    weather = info.find('weather')
    day = weather.find('day')
    for day_part in weather.iter('day_part'):
        if day_part.attrib['typeid'] == '2' and day_part.find('weather_code') is not None:
            current = day_part   
            return current
    return None

yandexData = downloadYandexFc()
yandexData = yandexData.encode('utf-8')
current = parseYandex ( yandexData )
print formatForecastYandex(current)

