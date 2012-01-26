#!/usr/bin/python
# -*- coding: utf-8 -*-

#* "THE BEER-WARE LICENSE" (Revision 42):
#* <john ät tuxcode dot org> wrote this file. As long as you retain this notice you
#* can do whatever you want with this stuff. If we meet some day, and you think
#* this stuff is worth it, you can buy me a beer in return.


import getopt, pynotify, sys , string, time

def std_notification(title, message):
	print ("%s :\n %s"%(title,message))

def db_notification(title, message) :
	try :
		pynotify.init("apyktt")
		n = pynotify.Notification(title,message,"appointment-soon")
		n.set_urgency(pynotify.URGENCY_NORMAL)
		n.set_timeout(pynotify.EXPIRES_NEVER)
		n.show()
	except Exception, e :
		print("kein dbus notify möglich")
		std_notification(title,message)

def usage():
	print("""
	   Aufruf: pyteatime  [OPTIONS] <seconds>
	   -h, --help                        zeigt diese Hilfe hier und beendet
	   -m, --message=<string>            gibt den notification string an
	   -t, --title=<string>              gibt den notification title an
	   -M, --minutes                     multipliziert den Zeitwert <seconds> mit 60 (can override -H)
	   -H, --hours                       multipliziert den Zeitwert mit 3600 (can override -M)
	   -c, --console                     deaktiviert dbus notification, schreibt auf stdout (mit sm benutzen!!!)
	   """)

def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "m:t:hMHc", ["help", "minutes" , "hours","console","message=","title="])
	except getopt.GetoptError, err:
		# print help information and exit:
			print str(err) # will print something like "option -a not recognized"
			usage()
			sys.exit(2)
	message = "Der Tee ist ferdsch"
	title   = "Achtung, Achtung!"
	mulseconds = 1
	dbusout = 1
	consoleout = 0
	for o, a in opts:
		if o in ("-h", "--help"):
			usage()
			sys.exit()
		elif o in ("-m", "--output"):
			message = a
		elif o in ("-t", "--title"):
			title = a
		elif o in ("-M","-H", "--minutes" , "--hours"):
			mulseconds = (o in ("-M","--minutes")) and 60 or 3600 
		elif o in ("-c","--console"):
			dbusout = 0
			consoleout = 1
		else:
			assert False, "unhandled option"

	try: 
		timearg = string.atoi(args[0])
	except Exception, e:
		print "Argument ist falsch!" , str(e)
		usage()
		sys.exit(2)

	time.sleep(timearg * mulseconds)
	if dbusout:
		db_notification(title,message)
		if consoleout:
			std_notification(title,message)

	sys.exit(0)

if __name__ == "__main__":
	main()

