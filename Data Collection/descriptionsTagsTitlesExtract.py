from googleapiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import json
import urllib2

#-----------------------------------------------------------------------------------------------------------

def main():
	mainDict = {}
	data = json.load(open('VideosPerChannel.json'))
	tcount = 0
	for channel in data:
		for id in data[channel]:
			tcount+=1.0
	print 'TOTAL: ',tcount
	count = 0.0
	for channel in data:
		mainDict[channel] = {}
		for id in data[channel]:
			getVid = True
			videoDict = {}
			while getVid:
				try:
					results = json.loads(urllib2.urlopen("https://www.googleapis.com/youtube/v3/videos?part=snippet&id=" + str(id[1][32:]) + "&fields=items(snippet(title,description,tags))&type=video&key=AIzaSyB84_YL94d4I_7ABN0ZCxnX10DxOQzAV74").read())
					getVid = False
				except urllib2.URLError,e:
					continue
				except Exception,e:
					print 'GetVideo Error:',str(e)
					break
			if getVid:
				continue
			try:
				videoDict['description'] = results['items'][0]['snippet']['description']
			except Exception,e:
				if str(e) == "'description'":
					videoDict['description'] = "No Description"
				else:
					print 'Description Error:',str(e)
			try:
				videoDict['tags'] = results['items'][0]['snippet']['tags']
			except Exception,e:
				if str(e) == "'tags'":
					videoDict['tags'] = "No Tags"
				else:
					print 'Tags Error:',str(e)
			try:
				videoDict['title'] = results['items'][0]['snippet']['title']
			except Exception,e:
				if str(e) == "'title'":
					videoDict['title'] = "No Title"
				else:
					print 'Title:',str(e)
			count += 1.0
			mainDict[channel][id[1][32:]] = videoDict
		print str(100*(count/tcount))[:4]+'% Complete'
	with open('tagsDescriptionsTitleChannel.json','w') as f:
		json.dump(mainDict,f)

#--------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
	main()





