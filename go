#! /usr/bin/env python
if __name__ == '__main__':
	import sys
	if sys.argv[1] == 'web':
		from web_control import webserver
		webserver.main()
	else:
		from iRobot import Create
		c = Create()
		c.set_device()
		c.connect()
		cmds = []
		for cmd in sys.argv[1:]:
			cmds.append(int(cmd))
		c.send(cmds)
