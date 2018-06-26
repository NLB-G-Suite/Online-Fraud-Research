import json

data = json.load(open('ldaOn_ad_click.json'))
allChannelVideos = json.load(open('VideosPerChannel.json'))

countDict = {}

for channel in data:
	countDict[channel] = 0.0
	for video in allChannelVideos[channel]:
		if ((' Ad ' in video[0] or ' Ad-' in video[0] or' ad ' in video[0] or ' ad-' in video[0]) and ('Click' in video[0] or 'click' in video[0])) or 'Click' in video[0] or 'click' in video[0]:
			countDict[channel] += 1.0

for channel in countDict:
	countDict[channel] = (countDict[channel],len(allChannelVideos[channel]),(countDict[channel]/len(allChannelVideos[channel])) * 100)

with open('PercentageFraudPerUser.json', 'w') as f:
	json.dump(countDict, f)

temp = 'Channel Hyperlink: (Fraudulent Videos, Total Videos, Percentage Fraudulent)\n\n'
for channel in countDict:
	temp += 'https://www.youtube.com/channel/'+str(channel)+': '+str(countDict[channel])+'\n'
with open('PercentageFraudPerUser.txt','w') as f:
	f.write(temp)
