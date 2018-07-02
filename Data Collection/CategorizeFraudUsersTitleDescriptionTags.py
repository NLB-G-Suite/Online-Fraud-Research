import json

data = json.load(open('ldaonTitleDescriptionTagsResults.json'))
fraudChannelsTitle = {}
txtDataTitle = ''
fraudChannelsDescription = {}
txtDataDescription = ''
fraudChannelsTag = {}
txtDataTag = ''

for channels in data:
	try:
		temp = []
		for ldaResults in data[channels]["title"]:
			# print ldaResults[1]
			if ((' ad ' in ldaResults[1] or ' ad-' in ldaResults[1]) and 'click' in ldaResults[1]) or 'click' in ldaResults[1]:
				temp.append(ldaResults[1])
		if len(temp) > 1:
			fraudChannelsTitle[channels] = temp
			txtDataTitle += 'https://www.youtube.com/channel/'+str(channels)+': '+str(temp)+'\n'
	except Exception,e:
		print str(e) 

	try:
		temp = []

		for ldaResults in data[channels]["description"]:
			# print ldaResults[1]
			if ((' ad ' in ldaResults[1] or ' ad-' in ldaResults[1]) and 'click' in ldaResults[1]) or 'click' in ldaResults[1]:
				temp.append(ldaResults[1])
		if len(temp) > 1:
			fraudChannelsDescription[channels] = temp
			txtDataDescription += 'https://www.youtube.com/channel/'+str(channels)+': '+str(temp)+'\n'
	except Exception,e:
		print str(e) 

	try:
		temp = []
		
		for ldaResults in data[channels]["tags"]:
			# print ldaResults[1]
			if ((' ad ' in ldaResults[1] or ' ad-' in ldaResults[1]) and 'click' in ldaResults[1]) or 'click' in ldaResults[1]:
				temp.append(ldaResults[1])
		if len(temp) > 1:
			fraudChannelsTag[channels] = temp
			txtDataTag += 'https://www.youtube.com/channel/'+str(channels)+': '+str(temp)+'\n'
	except Exception,e:
		print str(e) 
with open('ldaOn_ad_clickTitles.json','w') as f:
	json.dump(fraudChannelsTitle,f)

with open('ldaOn_ad_clickTitles.txt','w') as f:
	f.write(txtDataTitle)

with open('ldaOn_ad_clickDescription.json','w') as f:
	json.dump(fraudChannelsDescription,f)

with open('ldaOn_ad_clickDescription.txt','w') as f:
	f.write(txtDataDescription)

with open('ldaOn_ad_clickTag.json','w') as f:
	json.dump(fraudChannelsTag,f)

with open('ldaOn_ad_clickTag.txt','w') as f:
	f.write(txtDataTag)
