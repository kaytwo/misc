#!/usr/bin/python3

from json import loads
from os import system
from time import sleep
import requests
import os, pwd, grp

def drop_privileges(uid_name='nobody', gid_name='nogroup'):
  if os.getuid() != 0:
    # We're not root so, like, whatever dude
    return

  # Get the uid/gid from the name
  running_uid = pwd.getpwnam(uid_name).pw_uid
  running_gid = grp.getgrnam(gid_name).gr_gid

  # Remove group privileges
  os.setgroups([])

  # Try setting the new uid/gid
  os.setgid(running_gid)
  os.setuid(running_uid)


drop_privileges()

with open("/home/ckanich/workspace/misc/i3status/forecast.apikey") as f:
  apikey = f.read().strip()
location = "41.869791,-87.648339"
endpoint = "https://api.forecast.io/forecast/{0}/{1}"
forecasts = "currently","minutely","hourly","daily"


while True:
  screen_on = system("xset q | grep -Fxq '  Monitor is On'")
  if screen_on == 0:
    info = loads(requests.get(endpoint.format(apikey,location)).text)
    with open('/dev/shm/forecast','w') as f:
      f.write('{ "full_text": "%s°" },' % info['currently']['temperature'])
      for t in forecasts:
        f.write('{ "full_text": "%s" },' % info[t]['summary'])
    sleep(60)
  else:
    sleep(5)
