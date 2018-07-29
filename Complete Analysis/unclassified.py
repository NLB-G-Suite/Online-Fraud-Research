import csv
import json

keys=['videoId',
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
				'linksUp']
dict={}
with open('unclassified.csv', 'r') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
	for i in range(len(keys)):
		dict[keys[i]]=[]

	for row in spamreader:
		# dict['videoId']=row[0]
		for i in range(len(row)):
			# print keys[i],row[i]
			dict[keys[i]].append(row[i])
print dict
		# print len(row)
			# temp+=str(row)
with open('unclassified.json', 'w') as file:
        json.dump(dict, file)

		# print row