import json
import csv
import re
import url
import urllib2

x = json.load(open('crawlerResult.json'))

links=[]
linkcount=[]
category=[]
linksdown=[]
classification=[]

notclassified=0

count=0.0
for i in range(len(x['videoId'])):
	count += 1.0
	print str(100*(count/923.0))[:4]+'%'

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
	print linkList
	for link in linkList:
		if url.Active(link)=='not active':
			# print url.Active(link)
			inactive+=1
	linksdown.append(inactive)

	if len(linkList)!=0:
		links.append(linkList)
		linkcount.append(str(len(linkList)))

	else:
		links.append('No links')
		linkcount.append('0')

	with open ('categorylist.txt','r') as file:
		for line in file:
			if x['categoryId'][i] in str(line[0:4]):
				category.append(line[4:-1])
				break

	
x['links']=links
x['category']=category
x['linkcount']=linkcount
x['linksdown']=linksdown
x['classification']=classification

print 'not classified',notclassified

with open('csvdata.json', 'w') as fp:
	json.dump(x, fp)