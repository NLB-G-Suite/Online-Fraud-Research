import json
import sys

data = json.load(open('data2.json'))
cat = json.load(open('CategoryCount.json'))

temp=""
with open ('benigncategories.txt','w') as f:
	for i in range(len(data["title"])):
		print data["title"][i].encode(sys.stdout.encoding, errors='replace')

		temp+='Title: '+(data["title"][i].encode(sys.stdout.encoding, errors='replace'))
		
		try:
			temp+='\n videoId: https://www.youtube.com/watch?v='+ (data["videoId"][i].encode(sys.stdout.encoding, errors='replace'))
			temp+="\n channelTitle: "+ data["channelTitle"][i].encode(sys.stdout.encoding, errors='replace')
			# temp+='\n commentCount: '+ str(len(data["comments"][i]))
			# temp+='\n viewCount: '+ (data["viewCount"][i].encode(sys.stdout.encoding, errors='replace'))
			# print "category: ",data["category"][i].encode(sys.stdout.encoding, errors='replace')
			temp+="\n categoryId: "+ data["categoryId"][i].encode(sys.stdout.encoding, errors='replace')
			category_id= data["categoryId"][i].encode(sys.stdout.encoding, errors='replace')
			with open ('categorylist.txt','r') as file:
				for line in file:
					if category_id in line:
						temp+='\n category: '+ line[4:]
						break

				
			
			print "categoryId: ",data["categoryId"][i].encode(sys.stdout.encoding, errors='replace')
			print "videoId: ",data["videoId"][i].encode(sys.stdout.encoding, errors='replace')
			print len(data["comments"][i])
		except:
			print 'error'
		# for j in data["comments"][i]:
		# 	print j.encode(sys.stdout.encoding, errors='replace')
		# print data["comments"][i]
		temp+='\n\n'
		print "\n\n"
	f.write(temp)

