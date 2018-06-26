import json
import sys

data = json.load(open('data1.json'))
for i in range(len(data["title"])):
	print data["title"][i].encode(sys.stdout.encoding, errors='replace')
	for j in data["comments"][i]:
		print j.encode(sys.stdout.encoding, errors='replace')
	# print data["comments"][i]
	print "\n\n"

