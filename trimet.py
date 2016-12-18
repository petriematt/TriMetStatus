import requests
import json
import time

reply = requests.get('https://developer.trimet.org/ws/v2/arrivals?appid=755E5C1798BEC31002A57468D&locids=8375&arrivals=1&json=true')
sched = json.loads(reply.text)

currtime = time.time()
tooearly = currtime+300
toolate = currtime+600

for train in sched['resultSet']['arrival']:
	if train['status'] == 'estimated':
		#print 'Line: {route} is estimated'.format(route = train['route'])
		#print 'Line: {route} is estimated at {estimate}'.format(route = train['route'], estimate = time.ctime(float(train['estimated']/1000)))
		if (train['estimated']/1000) > tooearly and (train['estimated']/1000) < toolate:
			print '{route} at {estimate}'.format(route = train['shortSign'], estimate = time.ctime(float(train['estimated']/1000)))
	else:
		print 'Scheduled {line} - {time}'.format(line = train['shortSign'], time = time.ctime(float(train['scheduled']/1000)))



