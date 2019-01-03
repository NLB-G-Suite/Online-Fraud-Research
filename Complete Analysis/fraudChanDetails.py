import json
from googleapiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import urllib2
import sys
import threading
import time
from apiclient.discovery import build
import chanPages

DEVELOPER_KEY = 'AIzaSyB84_YL94d4I_7ABN0ZCxnX10DxOQzAV74'
youtube = build('youtube', 'v3', developerKey=DEVELOPER_KEY)

# channels = json.load(open('domainChannels.json'))
channels = json.load(open('fraudChannels.json'))

chan = {}
count=0
for channel in channels.keys():
# for channel in fraudChannels.keys():

	count+=1
	# print channel
	# if count>=6:
	# 	break
	while True:
		try:
			videos=chanPages.get_all_video_in_channel(channel)
			break
		except:
			time.sleep(5)
	print str(100*(count/float(len(channels.keys()))))[:4]+'%'

	title = []
	channelId = []
	channelTitle = []
	categoryId = []
	videoId = []
	viewCount = []
	commentCount = []
	category = []
	# videos = []
	comments = []
	tags = []
	uploadTime=[]
	description = []
	chan[channel]={}
	for i in range(len(videos)):
		videoId.append('https://www.youtube.com/watch?v='+videos[i])
		results = []
		result1=[]
		while True:
			try:
				results = youtube.videos().list(id=videos[i], part='snippet').execute()
				break
			except Exception,e:
				print e
				time.sleep(5)
		while True:
			try:
				result1 = youtube.videos().list(id=videos[i], part='statistics').execute()
				break
			except Exception,e:
				print e
				time.sleep(5)
		

		for result in result1.get('items', []):
			
			try:
				viewCount.append(result['statistics']['viewCount'])
			except:
				viewCount.append('No viewCount')
			
			try:
				commentCount.append(result['statistics']['commentCount'])
			except:
				commentCount.append('No commentCount')
		# print 'Result DONE'

		for result in results.get('items', []):
			title.append(result['snippet']['title'].encode('ascii','ignore')) 
			try:
				uploadTime.append(result['snippet']['publishedAt'])
			except:
				uploadTime.append('No time info')
			try:
				tags.append(result['snippet']['tags'])
			except:
				tags.append('No tags')
			try:
				description.append(result['snippet']['description'])
			except:
				description.append('No description')
			try:
				categoryId.append(result['snippet']['categoryId'])
			except:
				categoryId.append('No categoryId')
		try:
			commentsOnVideo = json.loads(urllib2.urlopen("https://www.googleapis.com/youtube/v3/commentThreads?key=AIzaSyB84_YL94d4I_7ABN0ZCxnX10DxOQzAV74&textFormat=plainText&part=snippet&videoId=" + videos[i] + "&maxResults=50",timeout=60).read())
			c = []
			for k in range(len(commentsOnVideo['items'])):
				c.append(commentsOnVideo['items'][k]["snippet"]['topLevelComment']['snippet']['textDisplay'])
			comments.append(c)
		except:
		    comments.append('No comments')



	print viewCount
	print uploadTime
	print commentCount
	chan[channel]['title']=title
	# chan[channel]['categoryId']=categoryId
	chan[channel]['videoId']=videoId
	chan[channel]['viewCount']=viewCount
	chan[channel]['time']=uploadTime
	# chan[channel]['comments']=comments
	chan[channel]['commentCount']=commentCount
	# chan[channel]['tags']=tags
	# chan[channel]['description']=description


# print chan.keys()
# with open('domainChannelsVids.json','w') as f:
# 	json.dump(chan,f)
with open('fraudChannelsVids.json','w') as f:
	json.dump(chan,f)
