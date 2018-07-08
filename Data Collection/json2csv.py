import json
import csv

x = json.load(open('crawlerResults.json'))

f = csv.writer(open("test.csv", "wb+"))

# Write CSV Header, If you dont need that, remove this line

f.writerow([y for y in x])

for i in range(len(x['videoId'])):
	try:
		f.writerow([x[y][i] for y in x])
	except:
		continue