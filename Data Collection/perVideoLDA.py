import json

data = json.load(open('ldaonTitleDescriptionTagsResults.json'))
fraudChannelsTitle = {}
fraudChannelsDescription = {}
fraudChannelsTag = {}

wordList = ['click','scam','profit click','profitclick',' ad ',' ad-','fraud','clickbank','per','pay','adclick']

for channels in data:
	try:
		temp = []
		flag = 0
		for ldaResults in data[channels]["title"]:
			for word in wordList:
				if word in ldaResults[1]:
					flag += 1
		if flag > 2:
			temp.append(ldaResults[1])
		if len(temp) > 1:
			fraudChannelsTitle[channels] = temp
	except Exception,e:
		print str(e) 

	try:
		temp = []
		for ldaResults in data[channels]["description"]:
			for word in wordList:
				if word in ldaResults[1]:
					flag += 1
		if flag > 2:
			temp.append(ldaResults[1])
		if len(temp) > 1:
			fraudChannelsDescription[channels] = temp
	except Exception,e:
		print str(e)  

	try:
		temp = []
		
		for ldaResults in data[channels]["tags"]:
			for word in wordList:
				if word in ldaResults[1]:
					flag += 1
		if flag > 2:
			temp.append(ldaResults[1])
		if len(temp) > 1:
			fraudChannelsTag[channels] = temp
	except Exception,e:
		print str(e)
		
with open('ldaOn_ad_clickTitles.json','w') as f:
	json.dump(fraudChannelsTitle,f)

with open('ldaOn_ad_clickDescription.json','w') as f:
	json.dump(fraudChannelsDescription,f)

with open('ldaOn_ad_clickTag.json','w') as f:
	json.dump(fraudChannelsTag,f)
