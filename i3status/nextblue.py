#!/usr/bin/python3

from json import loads
from os import system
import time
import requests
import os, pwd, grp
from lxml import etree
import urllib

stopid = 30068

endpoint = 'http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx?key={0}&stpid=30068'

with open("/home/ckanich/workspace/misc/i3status/traintracker.apikey") as f:
  apikey = f.read().strip()

def get_data():
  xml = etree.parse(urllib.urlopen(endpoint.format(apikey)))
  rets = []
  for item in xml.xpath('eta/arrT'):
    # 20130826 21:31:34
    stoptime = time.mktime(time.strptime(item.text,"%Y%m%d %H:%M:%S"))
    rets.append("%.1f minutes" % ((stoptime - time.time()) / 60))
  return "blue line to ORD: " + ", ".join(rets)

def check_forever():
  while True:
    screen_on = system("xset q | grep -Fxq '  Monitor is On'")
    if screen_on == 0:
      arrivaltext = get_data()
      with open('/dev/shm/nextblue','w') as f:
        f.write('{ "full_text": "%s" },' % arrivaltext)
      time.sleep(15)
    else:
      time.sleep(5)

check_forever()

