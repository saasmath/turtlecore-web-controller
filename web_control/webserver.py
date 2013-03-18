from os import path
from time import time
import subprocess
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from create import Create, FULL_MODE

base_path="/home/root/go/web_control/http/"
ip_address="192.168.0.109"
jquery='https://ajax.googleapis.com/ajax/libs/jquery/1.6.4/jquery.min.js' #'jquery.js' # with no internet

if __name__ == '__main__':
  main()

def main():
  try:
    vlc = setup_video()
    server = HTTPServer(('', 8090), CreateHandler)
    print 'started httpserver...'
    server.serve_forever()
  except KeyboardInterrupt:
    print '^C received, shutting down server'
    server.socket.close()
    vlc.terminate()
    vlc.wait()
    exit()

def setup_video(device='/dev/video7'):
  set_resolution = subprocess.Popen("v4l2-ctl -v width=160,height=120".split())
  set_resolution.wait()
  return subprocess.Popen(['cvlc', '--no-audio', 'v4l2://'+device+':width=160:height=120:fps=5:chroma=mjpg', '--sout=#standard{access=http,mux=mpjpeg,dst=0.0.0.0:8080}', '--sout-http-mime=multipart/x-mixed-replace;boundary=--7b3cc56e5f51db803f790dad720ed50a'])

controller = None
last_control = time()
c = Create('/dev/ttyO0', FULL_MODE)
drive_speed=0
turn_speed=0

class CreateHandler(BaseHTTPRequestHandler):
  def do_GET(self):
    global controller, last_control
    request_client = self.client_address[0]
    try:
      request, commands = self.path.split("?")
    except:
      if self.path == '/jquery.js':
        self.set_mime_type('text/javascript')
        self.send_file('jquery.js')
        return
      self.set_mime_type('text/html')
      if self.path == '/':
        if controller and time() - 60 < last_control:
          self.send_file('viewer.html')
        else:
          controller = request_client
          last_control = time()
          self.send_file('controller.html')
      return

    if controller == request_client:
      last_control = time()
      self.process_commands(commands)

  def process_commands(self, commands):
    global drive_speed, turn_speed, c
    command_list = commands.split("&")
    for command in command_list:
      name, value = command.split("=")
      value = int(value)
      if name == "drive":
        drive_speed = value*10
      elif name == "turn":
        turn_speed = value*5
    print "motor speed are: Left - ", drive_speed-turn_speed, ", Right - ", drive_speed+turn_speed
    c.driveDirect(drive_speed-turn_speed, drive_speed+turn_speed)

  def send_file(self, file):
    global base_path, ip_address, jquery
    full_path = path.join(base_path, file)
    print "Sending " + full_path
    html = open(full_path)
    self.wfile.write(html.read().replace("$$_IP_$$", ip_address).replace("$$_JQUERY_$$", jquery))
    html.close()

  def set_mime_type(self, type_name):
    self.send_response(200)
    self.send_header('Content-type', type_name)
    self.end_headers()
