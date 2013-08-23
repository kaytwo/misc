from json import loads
from os import system
from time import sleep
from urllib2 import urlopen

with open("forecast.apikey") as f:
  apikey = f.read().strip()
location = "41.869791,-87.648339"
endpoint = "https://api.forecast.io/forecast/%s/%s"
forecasts = "minutely","hourly","daily"


while True:
  screen_on = system("xset q | grep -Fxq '  Monitor is On'")
  if screen_on == 0:
    info = loads(urlopen(endpoint % (apikey,location)).read())
    for t in forecasts:
      print info[t]['summary']
  sleep(60)



