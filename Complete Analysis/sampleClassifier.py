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
		['ad','click'],
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
		'incom': 1,
		'paid': 1,
		'paytm': 1,
		'daily': 1,
		'admob': 3,
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
		'clickbank': 7,
		'adclick': 7,
		'adzbazar': 10,
		'paidvert': 10,
		'ptc': 7,
		'neobux': 8,
		'fortadpay': 10,
		'probux': 10,
		'clixsens': 10,
		'aurumclix': 10,
		'buxp': 10,
		'bigtimebux': 10,
		'adclickxpress': 10,
	}
	data = json.load(open('linkStatusBuffer.json'))
	data['classification'] = []
	suspect = {}

	for i in range(len(data['videoId'])):
		try:
			flag = 0
			wordFreq = {}
			for word in wordList:
				if word in data['title'][i]:
					flag +=1*wordList[word]
				for words in combinations:
					definiteFraud = 0
					for sensitive in words:
						if sensitive in data['tite'][i]:
							definiteFraud += 1
					if definiteFraud == len(words):
						flag += 20
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
				# if word in data['ldaDescriptionResults'][i]:
				if word in data['ldaDescriptionResults'][i]:
					flag +=1*wordList[word]
				# for tWord in data['ldaDescriptionResults'][i].lower().split():

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
		try:
			flag = 0
			if len(data['linksDown'][i]):
				uniqueLinks = []
				for link in data['linksDown'][i]:
					if link not in uniqueLinks:
						uniqueLinks.append(link)
						flag += 4
				# print flag
			if len(data['linksUp'][i]):
				uniqueLinks = []
				for link in data['scannedLink'][i]:
					if link not in uniqueLinks and 'result' not in data['scannedLink'][i][link]:
						uniqueLinks.append(link)
						flag += 10
			suspect[data['videoId'][i]].append([flag,[]])
		except Exception,e:
			print str(e)

	scoreDict = {}
	for video in suspect:
		finalScore = 0
		for score in suspect[video]:
			finalScore += score[0]
		scoreDict[video] = finalScore

	with open('sampleClassifier.json','w') as f:
		json.dump(scoreDict,f)
findPercentage()