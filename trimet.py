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
while 1:

	time.sleep(60)

	reply = requests.get('https://developer.trimet.org/ws/v2/arrivals?appid=755E5C1798BEC31002A57468D&locids=8375&arrivals=1&json=true')
	sched = json.loads(reply.text)

	currtime = time.time()
	tooearly = currtime+300
	toolate = currtime+600

	piglow.clear()

	for train in sched['resultSet']['arrival']:
		if train['status'] == 'estimated':
			if (train['estimated']/1000) > tooearly and (train['estimated']/1000) < toolate:
				#print '{route} at {estimate}'.format(route = train['shortSign'], estimate = time.ctime(float(train['estimated']/1000)))
				trainColor[train['route']]()
				#print '{route}'.format(route = train['route'])
		else:
			print 'Scheduled {line} - {time}'.format(line = train['shortSign'], time = time.ctime(float(train['scheduled']/1000)))

	piglow.show()


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

