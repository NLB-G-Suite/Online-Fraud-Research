import json

data = json.load(open('crawlerResultCheck.json'))
unique=[]

dict={}

count=0
# check=0
for i in range(len(data['videoId'])):
	check=0
	# if data['videoId'][i] not in dict.values():
	# 	dict[count]=[]
	# 	dict[count].append(data['videoId'][i])
	# 	count+=1
	# # else:
	for c in range(len(dict.keys())):
		if 'https://www.youtube.com/watch?v='+data['videoId'][i] in dict[c]:
			check=1
			dict[c].append('https://www.youtube.com/watch?v='+data['videoId'][i])
			break
	if check==0:
		dict[count]=[]
		dict[count].append('https://www.youtube.com/watch?v='+data['videoId'][i])
		count+=1
	

with open('repeatVideos.json','w') as f:
	json.dump(dict,f)

for i in range(len(data['videoId'])):
	if data['videoId'][i] not in unique:
		unique.append(data['videoId'][i])
print len(unique)
print len(data['videoId'])
