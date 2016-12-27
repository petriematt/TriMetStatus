import requests
import json
import time
import piglow
import os
import logging

#logging.basicConfig(filename='TriPi.log',level=logging.DEBUG)

#os.system("ping -c 10 -i 1 127.0.0.1")

def redLine():
	logging.debug('Red Line')
	piglow.red(255)

def blueLine():
	logging.debug('Blue Line')
	piglow.blue(255)

def greenLine():
	logging.debug('Green Line')
	piglow.green(255)

def errorStatus():
	logging.debug('Network Error')
	piglow.white(255)
	piglow.show()

trainColor = {	90 : redLine,
		100 : blueLine,
		200 : greenLine,
}

def checkInternet():
	logging.debug('Check Internet')
	pingstatus = 1
	while pingstatus != 0:
		pingstatus = os.system("ping -c 1 -i 1 trimet.org")
		if pingstatus != 0:	
			piglow.clear()
			piglow.show()
			errorStatus()

apiCounter = 0
logging.debug('Starting Program')
checkInternet()
while 1:


	if apiCounter == 0:
		
	
		#time.sleep(60)
		logging.debug('Getting Data from TriMet...')
		try:
			checkInternet()
			reply = requests.get('https://developer.trimet.org/ws/v2/arrivals?appid=755E5C1798BEC31002A57468D&locids=8375&arrivals=1&json=true')
			sched = json.loads(reply.text)
			currtime = time.time()
			tooearly = currtime+300
			toolate = currtime+600
			apiCounter = 60


			trainTable = []
			for train in sched['resultSet']['arrival']:
				if train['status'] == 'estimated':
					if (train['estimated']/1000) > tooearly and (train['estimated']/1000) < toolate:
						#trainColor[train['route']]()
						routenum = train['route']
						trainTable.append([routenum,'est','on'])
				else:
					if (train['scheduled']/1000) > tooearly and (train['scheduled']/1000) < toolate:
						routenum = train['route']
						trainTable.append([routenum,'sched','on'])
		
			piglow.clear()
			for color in trainTable:
				if color[1] == 'est':
					trainColor[color[0]]()
				else:
					if color[2] == 'on':
						trainColor[color[0]]()
						color[2] = 'off'
					else:
						color[2] = 'on'
			#print 'Next: {table} - new data in {nextcall} second(s).'.format(table = trainTable, nextcall = apiCounter)
			piglow.show()
		except:
			checkInternet()

	apiCounter -= 1
	time.sleep(1)


#
#
#
#
#
#
#
#
#
#
#
#
#
#

