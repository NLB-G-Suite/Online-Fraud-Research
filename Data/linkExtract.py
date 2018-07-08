from googleapiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import json
import urllib2
import re
import url

data = json.load(open('tagsDescriptionsTitleChannel.json'))
temp = ''

for channel in data:
	for id in data[channel]:
		try:
			data[channel][id]['links'] = url.check(data[channel][id]['description']+' ')
		except Exception, e:
			data[channel][id]['links'] = 'No links'
			continue

with open('TagsDescLinks.json','w') as f:
	json.dump(data,f)
