#!/usr/bin/env python

import requests
import sys

try:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    }
    r = requests.get('http://informer.gismeteo.ru/xml/34122.xml', headers=headers)
except requests.exceptions.RequestException as e:  # This is the correct syntax
    print e
    sys.exit(1)

try:
    f = open('gismeteo_voronezh.xml', 'w')
    f.write(r.text)
    f.close();
except:
    print "Unexpected error:", sys.exc_info()[0]
    raise

