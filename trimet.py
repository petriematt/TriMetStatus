import requests
import json
import time
import piglow

def redLine():
#	print 'Red'
	piglow.red(150)

def blueLine():
#	print 'Blue'
	piglow.blue(150)

def greenLine():
#	print 'Green'
	piglow.green(150)

trainColor = {	90 : redLine,
		100 : blueLine,
		200 : greenLine,
}

apiCounter = 0
while 1:
	
	if apiCounter == 0:
		
	
		#time.sleep(60)
		#print 'Getting Data from TriMet...'
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

