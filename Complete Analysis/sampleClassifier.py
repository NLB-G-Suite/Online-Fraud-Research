import json
import csv 

# littlebux.com
# fortadpay.com
# adf.ly
#

def findPercentage():
	uniqueChan = []
	countDict = {}
	
	combinations = [
		['paid','to','click'],
		['ad ','click'],
		['ad','view','money'],
		['ad','watch','money'],
		['ad','watch','earn'],
		['app','click','own'],
		['admob','vpn'],
		['admob','self','click'],
		['earn','click',' ad'],
		['money','click',' ad'],
		['self','click']
	]
	wordList = {
		'per': 1,
		'pay': 1,
		'link': 1,
		'paypal': 1,
		'paid': 1,
		'paytm': 1,
		'admob': 2,
		'cryptocurr': 1,
		'click': 4,
		'profit': 2,
		'money': 1,
		'profit click': 7,
		'earn': 1,
		'profitclick': 7,
		'ad ': 4,
		'btc': 2,
		'bitcoin': 2,
		' ads': 4,
		' ad ': 4,
		'advertis': 4,
		' ad-': 4,
		'adclick': 7,
		'adzbazar': 10,
		'paidvert': 10,
		'ptc': 7,
		'littlebux': 10,
		'neobux': 10,
		'pvtraffic': 10,
		'fortadpay': 10,
		'probux': 10,
		'clixsens': 10,
		'aurumclix': 10,
		'buxp': 10,
		'bigtimebux': 10,
		'adclickxpress': 10,
		'family click': 10
	}
	benign = [
	'scam',
	'fraud',
	'dropship',
	'train',
	'sell',
	'business'
	]
	safeCombinations = [
		'without click'
	]
	data = json.load(open('crawlerResult.json'))
	data['classification'] = []
	suspect = {}

	for i in range(len(data['videoId'])):
		print str(100*(float(i)/float(len(data['videoId']))))[:5]+'%'
		try:
			flag = 0
			wordFreq = {}
			for words in combinations:
				definiteFraud = 0
				for sensitive in words:
					if sensitive in data['title'][i].lower():
						definiteFraud += 1
				if definiteFraud == len(words):
					flag += 20
			for word in wordList:
				if word in data['title'][i].lower():
					flag += wordList[word]
				for tWord in data['title'][i].lower().split():
					if word in tWord:
						if word in wordFreq:
							wordFreq[word] += 1
						else:
							wordFreq[word] = 1
			suspect[data['videoId'][i]] = []
			suspect[data['videoId'][i]].append([flag,wordFreq])
		except Exception,e:
			print str(e) 
		try:
			flag = 0
			wordFreq = {}
			for word in wordList:
				if len(data['description'][i].split()) < 10 and word in data['description'][i].lower():
					flag += wordList[word]
				else:
					if word in data['ldaDescriptionResults'][i]:
						flag += wordList[word]

				for tWord in data['description'][i]:
					if word in tWord:
						if word in wordFreq:
							wordFreq[word] += 1
						else:
							wordFreq[word] = 1
			suspect[data['videoId'][i]].append([flag,wordFreq])
		except Exception,e:
			print str(e)
		try:
			flag = 0
			wordFreq = {}
			for word in wordList:
				check = 1
				for tag in data['tags'][i]:
					if word in tag.lower():
						if check:
							flag += wordList[word]
							check = 0
						if word in wordFreq:
							wordFreq[word] += 1
						else:
							wordFreq[word] = 1
			suspect[data['videoId'][i]].append([flag,wordFreq])
		except Exception,e:
			print str(e)
		# try:
		# 	flag = 0
		# 	if len(data['linksDown'][i]):
		# 		uniqueLinks = []
		# 		for link in data['linksDown'][i]:
		# 			if link not in uniqueLinks:
		# 				uniqueLinks.append(link)
		# 				flag += 2
		# 		# print flag
		# 	# if len(data['linksUp'][i]):
		# 	# 	uniqueLinks = []
		# 	# 	for link in data['scannedLink'][i]:
		# 	# 		if link not in uniqueLinks and 'result' not in data['scannedLink'][i][link]:
		# 	# 			uniqueLinks.append(link)
		# 	# 			flag += 10
		# 	suspect[data['videoId'][i]].append([flag,[]])
		# except Exception,e:
		# 	print str(e)

	scoreDict = {}
	for video in suspect:
		finalScore = 0
		for score in suspect[video]:
			finalScore += score[0]
		scoreDict[video] = finalScore
	for i in range(len(data['videoId'])):
		for word in safeCombinations:
			if scoreDict[data['videoId'][i]] > 0 and word in data['title'][i].lower():
				print data['title'][i].lower()
				scoreDict[data['videoId'][i]] *= -1
				print scoreDict[data['videoId'][i]]
		if scoreDict[data['videoId'][i]] > 0:
			for word in benign:
				if word in data['title'][i].lower():
					scoreDict[data['videoId'][i]] *= -1
					break

	with open('sampleClassifierScaled.json','w') as f:
		json.dump(scoreDict,f)

findPercentage()
