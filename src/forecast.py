#!/usr/bin/env python

import sys
import requests
import time
import xml.etree.ElementTree as ET
import max7219.led as led
from max7219.font import proportional, SINCLAIR_FONT, TINY_FONT, CP437_FONT

def downloadYandexFc():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    }
    r = requests.get('https://export.yandex.ru/bar/reginfo.xml?region=193', headers=headers)
    return r.text.encode('utf-8')

def formatForecastYandex( forecast ):
    wind_speed = forecast.find('wind_speed').text
    temperature = forecast.find('temperature').text
    return '%s%sC %sm/c' % (temperature, chr(0xF8), wind_speed)

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

def formatForecastGismeteo( forecast ):
   temp = forecast.find('HEAT')
   tMax = temp.attrib['max']
   tMin = temp.attrib['min']

   pressure = forecast.find('PRESSURE')
   pMax = pressure.attrib['max']
   pMin = pressure.attrib['min']

   wind = forecast.find('WIND')
   wMax = wind.attrib['max']
   wMin = wind.attrib['min']

   return '%s%sC %s%sC %s-%sm/c' % (tMin, chr(0xF8), tMax, chr(0xF8), wMin, wMax)

def download_fc():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    }
    r = requests.get('http://informer.gismeteo.ru/xml/34122.xml', headers=headers)
    return r.text

device = led.matrix(cascaded=4, spi_bus=0, spi_device=0, vertical=True)

while True:
    print "process new iteration"
    try:
        print "download forecast"
        fc_text = download_fc()
        root = ET.fromstring(fc_text)
    except:
        err = "Err:", sys.exc_info()[0]
        print "download forecast failed"
        print err
        device.show_message(err, font=proportional(CP437_FONT))
        time.sleep(10)
        continue

    try:
        yandexData = downloadYandexFc()
        currentYandex = parseYandex ( yandexData )
    except:
        currentYandex = None
        err = "Err:", sys.exc_info()[0]
        print "download yandex forecast failed"
        print err


    fc0 = formatForecastGismeteo(root[0][0][0])
    if currentYandex != None:    
        fcYa = formatForecastYandex(currentYandex)
        fc0 = "yandex %s gismeteo %s" % (fcYa, fc0)

    fc1 = '>%s' % formatForecastGismeteo(root[0][0][1])
    fc2 = '>>%s' % formatForecastGismeteo(root[0][0][2])

    for x in range(100):
        device.brightness(15)
        device.show_message(fc0, font=proportional(CP437_FONT))
        time.sleep(3)

        if '--showfc' in sys.argv:
            device.brightness(1)
            device.show_message(fc1)
            time.sleep(1)

            device.show_message(fc2)
            time.sleep(1)

            #fc = '%s %s %s' % (fc0, fc1, fc2)
            #device.show_message(fc)

