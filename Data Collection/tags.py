from googleapiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import json
import urllib2

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
		for id in data[channel]:
			try:
				results = json.loads(urllib2.urlopen("https://www.googleapis.com/youtube/v3/videos?part=snippet&id=" + str(id[1][32:]) + "&type=video&key=AIzaSyB84_YL94d4I_7ABN0ZCxnX10DxOQzAV74").read())
				mainDict[id[1][32:]] = results['items'][0]['snippet']['tags']
			except Exception,e:
				if str(e) == "'tags'":
					mainDict[id[1][32:]] = "No Tags"
				else:
					print str(e)
			count += 1.0
		print str(100*(count/tcount))[:4]+'% Complete'
	with open('videoTags.json','w') as f:
		json.dump(mainDict,f)

if __name__ == "__main__":
	main()
