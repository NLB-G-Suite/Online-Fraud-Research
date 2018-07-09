import json
import csv

x = json.load(open('crawlerResult.json'))
f = csv.writer(open("test.csv", "wb+"))

f.writerow(
			['videoId',
			'title',
			'channelId',
			'viewCount',
			'commentCount',
			'comments',
			'tags',
			'description',
		])

for i in range(len(x['videoId'])):
	try:
		f.writerow(
			['https://www.youtube.com/watch?v='+x['videoId'][i],
			x['title'][i].encode('ascii','ignore'),
			x['channelId'][i],
			x['viewCount'][i],
			x['commentCount'][i],
			x['comments'][i],
			x['tags'][i],
			x['description'][i].encode('ascii','ignore'),
		])
	except Exception,e:
		print str(e)