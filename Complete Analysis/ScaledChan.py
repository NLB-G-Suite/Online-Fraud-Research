import json
from googleapiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import requests
import sys
import threading
import time
from apiclient.discovery import build
import chanPages

# DEVELOPER_KEY = 'AIzaSyB84_YL94d4I_7ABN0ZCxnX10DxOQzAV74'
youtube = build('youtube', 'v3', developerKey=DEVELOPER_KEY)

count=0

def chanVids(DEVELOPER_KEY,channels,chan):
	for channel in channels:
		# count+=1
		while True:
			try:
				videos=chanPages.get_all_video_in_channel(channel)
				break
			except:
				time.sleep(5)
		# print str(100*(count/float(len(channels.keys()))))[:4]+'%'
		print threading.currentThread().getName()
        # +' ' +str(100*(count/float(numOfResults)))[:4]+'%'

		title = []
		channelId = []
		channelTitle = []
		categoryId = []
		videoId = []
		viewCount = []
		commentCount = []
		category = []
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
					# print e
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
				commentsOnVideo = json.loads(requests.get("https://www.googleapis.com/youtube/v3/commentThreads?key=AIzaSyB84_YL94d4I_7ABN0ZCxnX10DxOQzAV74&textFormat=plainText&part=snippet&videoId=" + videos[i] + "&maxResults=50",timeout=60).read())
				c = []
				for k in range(len(commentsOnVideo['items'])):
					c.append(commentsOnVideo['items'][k]["snippet"]['topLevelComment']['snippet']['textDisplay'])
				comments.append(c)
			except:
			    comments.append('No comments')

		chan[channel]['title']=title
		chan[channel]['videoId']=videoId
		chan[channel]['viewCount']=viewCount
		chan[channel]['time']=uploadTime
		chan[channel]['commentCount']=commentCount
	with open('scaledChan'+threading.currentThread().getName()+'.json','w') as f:
		json.dump(chan,f)
	print threading.currentThread().getName()+'  DONE'


channels=[]
dataScaled = json.load(open('uniqueScaled.json'))
for i in range(len(dataScaled['videoId'])):
	if dataScaled['predClass'][i]=='f':
		if dataScaled['channelId'][i] not in channels:
			channels.append(dataScaled['channelId'][i])
print channels			
print len(channels)
chan = {}
count=0
keys=[]

with open('apiKeys.txt','r') as f:
	for line in f:
		if str(line[:-1]) not in keys:
			keys.append(str(line[:-1]))

threads=[threading.Thread(target=chanVids,args=(keys[x],channels[130*x:130*x+130],chan)) for key in keys]
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
# for x in range(50):
# 	threading.Thread(name=str(x),target=chanVids,args=(keys[x],channels[130*x:130*x+130],chan)).start()

# with open('scaledChanVids.json','w') as f:
# 	json.dump(chan,f)
