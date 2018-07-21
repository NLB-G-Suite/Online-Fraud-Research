import json
import csv

def csvConvert():
	x = json.load(open('linkStatusBuffer(1).json'))
	Scores = json.load(open('sampleClassifier.json'))
	notclassified=0
	totalMalLinks=[]
	# scanlinks=0
	for i in range(len(x['videoId'])):
		maliciousLinks = []
		if len(x['linksUp'][i]):
			for link in x['scannedLink'][i]:
				if 'result' not in x['scannedLink'][i][link]:
					tempDict={}
					tempDict[link]=x['scannedLink'][i][link]
					maliciousLinks.append(tempDict)
		totalMalLinks.append(maliciousLinks)

		classify=0
		title=x['title'][i].encode('ascii','ignore')
		with open ('manuallyLabelled.txt','r') as f:
			for line in f:
				if title in line:
					classify=1
					if line[0]=='b':
						x['classification'][i]='b'
					if line[0]=='f':
						x['classification'][i]='f'
					break
			if classify==0:
				notclassified+=1
				x['classification'][i]='Not classified'
	x['totalMalLinks']=totalMalLinks
	with open('linkStatusBuffer(1).json','w') as f:
		json.dump(x,f)
		
	f = csv.writer(open("linkStatusBufferGithub.csv", "wb+"))

	f.writerow(
				['videoId',
				'title',
				'channelId',
				'category',
				'classification',
				'viewCount',
				'commentCount',
				'comments',
				'tags',
				'description',
				'links',
				'linksCount',
				'linksDownCount',
				'linksDown',
				'linksUp',
				'ScannedLinks',
				'maliciousLinks',
				'FraudScore'
			])

	for i in range(len(x['videoId'])):
		try:
			f.writerow(
				['https://www.youtube.com/watch?v='+x['videoId'][i],
				x['title'][i].encode('ascii','ignore'),
				x['channelId'][i],
				x['category'][i],
				x['classification'][i],
				x['viewCount'][i],
				x['commentCount'][i],
				x['comments'][i],
				x['tags'][i],
				x['description'][i].encode('ascii','ignore'),
				x['links'][i],
				x['linksCount'][i],
				x['linksDownCount'][i],
				x['linksDown'][i],
				x['linksUp'][i],
				x['scannedLink'][i],
				x['totalMalLinks'][i],
				Scores[x['videoId'][i]]
			])
		except Exception,e:
			print str(e)
csvConvert()