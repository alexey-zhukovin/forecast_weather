# weather forecast
connect matrix to RPI doc:
https://geektimes.ru/post/271058/

GISMETEO:
https://gist.github.com/ikenfin/85f15f42a6790a86d56b193cadc296ae
http://informer.gismeteo.ru/rss/34122.xml
http://informer.gismeteo.ru/xml/34122.xml

YANDEX:
https://export.yandex.ru/bar/reginfo.xml?region=193

```sh
$ sudo apt-get install python-dev python-pip
$ sudo pip install spidev
$ sudo python setup.py install
$ sudo nano /etc/rc.local
$ chgrp -R dialout /sys/class/gpio
$ chmod -R g+rw /sys/class/gpio
```

The gpio group was before

Raspberry PI MAX7219 driver:
```sh
git clone https://github.com/rm-hull/max7219.git
```
http://homeway.me/2015/04/29/openwrt-develop-base-util/


