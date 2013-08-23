#!/usr/bin/python
'''
Consume audioscrobbles and push them into shm to display in i3bar
'''
import SimpleHTTPServer
import socket
import SocketServer
import threading
from time import sleep
from urlparse import parse_qs

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

  # Ensure a very conservative umask
  # old_umask = os.umask(077)


PORT = 80
HOST = "127.0.1.1"

def wipe(timeout):
  sleep(timeout)
  with open('/dev/shm/current_song','w') as f:
      f.truncate()

class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

  def do_POST(self):
    content_len = int(self.headers.getheader('content-length'))
    pbody = parse_qs(self.rfile.read(content_len))
    self.send_response(200)
    self.end_headers()
    self.wfile.write('OK\n')
    try:
      artist,title,length = [pbody[x][0] for x in ('a','t','l')]
      with open('/dev/shm/current_song','w') as f:
        f.write("%s - %s" % (artist,title))
      t = threading.Thread(target=wipe,args=(int(length)-1,))
      t.daemon = True
      t.start()
    except:
      # fake an authenticate response
      self.wfile.write("1161735e927d40ef81bccad822a3de18\nhttp://post.audioscrobbler.com:80/np_1.2\nhttp://post.audioscrobbler.com:80/protocol_1.2\n")
      pass


httpd = SocketServer.TCPServer((HOST,PORT),ServerHandler)
httpd.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
drop_privileges()
httpd.serve_forever()
