import json
import csv

def csvConvert():
	x = json.load(open('csvdataBuffer.json'))
	f = csv.writer(open("testBuffer.csv", "wb+"))

	f.writerow(
				['videoId',
				'title',
				'channelId',
				'category',
				'classification',
				'viewCount',
				'commentCount',
				'comments',
				'tags',
				'description',
				'links',
				'linksCount',
				'linksDownCount',
				'linksDown',
				'linksUp'
			])

	for i in range(len(x['videoId'])):
		try:
			f.writerow(
				['https://www.youtube.com/watch?v='+x['videoId'][i],
				x['title'][i].encode('ascii','ignore'),
				x['channelId'][i],
				x['category'][i],
				x['classification'][i],
				x['viewCount'][i],
				x['commentCount'][i],
				x['comments'][i],
				x['tags'][i],
				x['description'][i].encode('ascii','ignore'),
				x['links'][i],
				x['linksCount'][i],
				x['linksDownCount'][i],
				x['linksDown'][i],
				x['linksUp'][i]
			])
		except Exception,e:
			print str(e)