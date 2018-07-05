from googleapiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import json
import urllib2
import re

data = json.load(open('tagsDescriptionsTitleChannel.json'))
temp = ''
for channel in data:
	for id in data[channel]:
		try:
			data[channel][id]['links'] = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',data[channel][id]['description'])
			temp+=str(data[channel][id]['links'])+'\n'
		except:
			continue

with open('TagsDescLinks.json','w') as f:
	json.dump(data,f)

with open('TagsDescLinks.txt','w') as f:
	f.write(temp)