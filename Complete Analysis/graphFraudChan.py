import json
import datetime
# from datetime import date

channels = json.load(open('fraudChannelsVids.json'))
fraudChan = json.load(open('fraudChannels.json'))

# date_format = '%Y-%m-%d'
# a = datetime.strptime('2008-18-8', date_format)
# b = datetime.strptime('2008-18-10', date_format)

# b = datetime.datetime.today().strftime('%Y-%m-%d')
# print b
# delta = b - a
# print delta.days

# time_chan="2018-11-29T14:05:35.000Z"
# someday = datetime.date(int(time_chan[0:4]), int(time_chan[5:7]), int(time_chan[8:10]))
# print someday
# diff = today - someday
# print diff.days

today = datetime.date.today()
anomaly={}
for channel in channels:
	viewCount=[]
	somedays=[datetime.date(int(x[0:4]), int(x[5:7]), int(x[8:10])) for x in channels[channel]['time']]
	fraudChan[channel]['time']=[int(str((today-someday).days)) for someday in somedays]
	fraudChan[channel]['commentCount']=[0 if x=='No commentCount' else int(x) for x in channels[channel]['commentCount']]
	viewCount=[0 if x=='No viewCount' else int(x) for x in channels[channel]['viewCount']]
	fraudChan[channel]['viewCount']=[]
	anomaly[channel]=[]
	for view in viewCount:
		if view>=100000:
			anomaly[channel].append(view)
		else:
			fraudChan[channel]['viewCount'].append(view)
	# fraudChan[channel]['maxComments']=max(channels[channel]['commentCount'])
	# fraudChan[channel]['minComments']=min(channels[channel]['commentCount'])
	# fraudChan[channel]['avgComments']=sum(channels[channel]['commentCount'])/len(channels[channel]['commentCount'])
	
	# fraudChan[channel]['maxViews']=max(channels[channel]['viewCount'])
	# fraudChan[channel]['minViews']=min(channels[channel]['viewCount'])
	# fraudChan[channel]['avgViews']=sum(channels[channel]['viewCount'])/len(channels[channel]['viewCount'])

	# fraudChan[channel]['maxtimeDiff']=max(channels[channel]['time'])
	# fraudChan[channel]['mintimeDiff']=min(channels[channel]['time'])
	# fraudChan[channel]['avgtimeDiff']=sum(channels[channel]['time'])/len(channels[channel]['time'])

with open('graphChannels2.json','w') as f:
	json.dump(fraudChan,f)

