from os import system

class Create:
	def set_device(self, device='/dev/ttyO0'):
		self.device = device
	def connect(self):
		system('stty -F ' + self.device + ' ispeed 57600 cs8 -cstopb -brkint -icrnl -imaxbel -opost -onlcr -isig -icanon -iexten -echo -echoe -echok -echoctl -echoke')
	def send(self, values):
		f = open(self.device, 'w')
		for value in values:
			f.write(chr(value))
		f.close()
