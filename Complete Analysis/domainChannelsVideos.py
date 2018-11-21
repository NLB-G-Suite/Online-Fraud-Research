import json
from googleapiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import urllib2
import sys
import threading
import time
from apiclient.discovery import build

DEVELOPER_KEY = 'AIzaSyClserQ1cuNOX9SssQT6-BvBf65JZZ1Lk4'
youtube = build('youtube', 'v3', developerKey=DEVELOPER_KEY)

channels = json.load(open('domainChannels.json'))

chan = {}
count=0
for channel in channels.keys():

	print "channel"
	chanVids = json.loads(urllib2.urlopen("https://www.googleapis.com/youtube/v3/search?key=AIzaSyClserQ1cuNOX9SssQT6-BvBf65JZZ1Lk4&channelId="+channel+"&part=snippet,id&order=date&maxResults=50").read())
	# d = []
	print str(100*(count/float(len(channels.keys()))))[:4]+'%'

	title = []
	channelId = []
	channelTitle = []
	categoryId = []
	videoId = []
	viewCount = []
	commentCount = []
	category = []
	videos = []
	comments = []
	tags = []
	description = []
	chan[channel]={}
	for k in range(len(chanVids['items'])):
		if 'videoId' in chanVids['items'][k]['id']:
			videoId.append('https://www.youtube.com/watch?v='+chanVids['items'][k]['id']['videoId'])
			results = youtube.videos().list(id=chanVids['items'][k]['id']['videoId'], part='snippet').execute()
			for result in results.get('items', []):

				title.append(result['snippet']['title']) 
				try:
					categoryId.append(result['snippet']['categoryId'])
				except:
					categoryId.append('No categoryId')
				try:
					viewCount.append(result['statistics']['viewCount'])
				except:
					viewCount.append('No viewCount')
				try:
					tags.append(result['snippet']['tags'])
				except:
					tags.append('No tags')
				try:
					description.append(result['snippet']['description'])
				except:
					description.append('No description')
			try:
				commentsOnVideo = json.loads(urllib2.urlopen("https://www.googleapis.com/youtube/v3/commentThreads?key=AIzaSyB84_YL94d4I_7ABN0ZCxnX10DxOQzAV74&textFormat=plainText&part=snippet&videoId=" + chanVids['items'][k]['id']['videoId'],timeout=60).read())
				c = []
				for k in range(len(commentsOnVideo['items'])):
					c.append(commentsOnVideo['items'][k]["snippet"]['topLevelComment']['snippet']['textDisplay'])
				comments.append(c)
			except:
			    comments.append('No comments')
			try:
			    if 'commentCount' in chanVids['items'][k]['statistics'].keys():
			        commentCount.append(chanVids['items'][k]['statistics']['commentCount'])
			    else:
			        commentCount.append("No commentCount")
			except:
			    commentCount.append("No commentCount")

	chan[channel]['title']=title
	chan[channel]['categoryId']=categoryId
	chan[channel]['videoId']=videoId
	chan[channel]['viewCount']=viewCount
	chan[channel]['commentCount']=commentCount
	chan[channel]['comments']=comments
	chan[channel]['tags']=tags
	chan[channel]['description']=description


	# break
print chan.keys()
with open('domainChannelsVids.json','w') as f:
	json.dump(chan,f)		        
# if response['items'][0]['snippet']['channelId'] not in chan:
#     chan[response['items'][0]['snippet']['channelId']] = d