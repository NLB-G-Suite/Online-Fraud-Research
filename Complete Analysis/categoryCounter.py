import json
import sys

# data = json.load(open('data2.json'))

temp=""
categories = []
count ={}

for i in range(len(data["title"])):	
	try:
		category_id= data["categoryId"][i].encode(sys.stdout.encoding, errors='replace')
		with open ('categorylist.txt','r') as file:
			for line in file:
				if category_id in line:
					if line[4:] not in categories:
						categories.append(line[4:])
						count[line[4:]] = 0
					else:
						count[line[4:]] += 1
					break
	except:
		print 'error'
	# for j in data["comments"][i]:
	# 	print j.encode(sys.stdout.encoding, errors='replace')
	# print data["comments"][i]
with open('CategoryCount.json','w') as f:
	json.dump(count,f)

temp=""
with open('CategoryCount.txt','w') as f:
	for ele in categories:
		temp +=	ele[:-1]+': '+str(count[ele])+"\n"
	f.write(temp)
