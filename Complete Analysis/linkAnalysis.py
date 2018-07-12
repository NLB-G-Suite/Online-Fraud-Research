import json
import csv
import re
import url
import urllib2
import httplib2

def linkWork(nres):
	x = json.load(open('crawlerResult.json'))

	links=[]
	linksCount=[]
	category=[]
	linksDownCount=[]
	linksDown = []
	linksUp = []
	classification=[]

	notclassified=0

	count=0.0
	h = httplib2.Http(timeout=60)
	for i in range(len(x['videoId'])):
		count += 1.0
		print str(100*(count/float(nres)))[:4]+'%'

		classify=0
		title=x['title'][i].encode('ascii','ignore')
		with open ('manuallyLabelled.txt','r') as f:
			for line in f:
				if title in line:
					classify=1
					if line[0]=='b':
						classification.append('b')
					if line[0]=='f':
						classification.append('f')
					break
			if classify==0:
				notclassified+=1
				classification.append('Not classified')

		linkList=url.check(x['description'][i]+' ')
		inactive=0
		videoLinksUp = []
		videoLinksDown = []
		for link in linkList:
			result = url.active(link,h)
			if result =='not active':
				inactive+=1
				videoLinksDown.append(link)
			else:
				videoLinksUp.append(link)
		linksDownCount.append(inactive)
		linksDown.append(videoLinksDown)
		linksUp.append(videoLinksUp)

		if len(linkList)!=0:
			links.append(linkList)
			linksCount.append(str(len(linkList)))

		else:
			links.append('No links')
			linksCount.append('0')

		with open ('categorylist.txt','r') as file:
			for line in file:
				if x['categoryId'][i] in str(line[0:4]):
					category.append(line[4:-1])
					break

		
	x['links']=links
	x['category']=category
	x['linksCount']=linksCount
	x['linksDown'] = linksDown
	x['linksUp'] = linksUp
	x['linksDownCount']=linksDownCount
	x['classification']=classification

	with open('linkStatus.json', 'w') as fp:
		json.dump(x,fp)