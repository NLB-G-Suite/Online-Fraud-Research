import json

titles = json.load(open('ldaOn_ad_clickTitles.json'))
descs = json.load(open('ldaOn_ad_clickDescription.json'))
tags = json.load(open('ldaOn_ad_clickTag.json'))

uniqueChan = []

for channel in titles:
	uniqueChan.append(channel)

for channel in descs:
	if channel not in uniqueChan:
		uniqueChan.append(channel)

for channel in tags:
	if channel not in uniqueChan:
		uniqueChan.append(channel)

print len(uniqueChan),':',uniqueChan
