#!/usr/bin/python3

from json import loads
from os import system
from time import sleep
import requests

with open("forecast.apikey") as f:
  apikey = f.read().strip()
location = "41.869791,-87.648339"
endpoint = "https://api.forecast.io/forecast/{0}/{1}"
forecasts = "minutely","hourly","daily"


while True:
  screen_on = system("xset q | grep -Fxq '  Monitor is On'")
  if screen_on == 0:
    info = loads(requests.get(endpoint.format(apikey,location)).text)
    with open('/dev/shm/forecast','w') as f:
      for t in forecasts:
        f.write('{ "full_text": "%s" },' % info[t]['summary'])
    sleep(60)
  else:
    sleep(5)
