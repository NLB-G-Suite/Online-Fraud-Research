import json

data = json.load(open('ldaTitleResults.json'))
fraudChannels = {}
txtData = ''
for channels in data:
	temp = []
	for ldaResults in data[channels]:
		if ((' ad ' in ldaResults[1] or ' ad-' in ldaResults[1]) and 'click' in ldaResults[1]) or 'click' in ldaResults[1]:
			temp.append(ldaResults[1])
	if len(temp) > 1:
		fraudChannels[channels] = temp
		txtData += 'https://www.youtube.com/channel/'+str(channels)+': '+str(temp)+'\n'
 
with open('ldaOn_ad_click.json','w') as f:
	json.dump(fraudChannels,f)

with open('ldaOn_ad_click.txt','w') as f:
	f.write(txtData)
