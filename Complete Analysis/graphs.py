import json
import csv 


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
data = json.load(open('linkStatusBuffer(1).json'))

Graph={}
Graph['fraud']={}
Graph['benign']={}
Graph['fraud']['title'] ={}
Graph['fraud']['description'] ={}
Graph['fraud']['tags'] ={}
Graph['benign']['title'] ={}
Graph['benign']['description'] ={}
Graph['benign']['tags'] ={}
fwordCount=0
bwordCount=0

for i in range(len(data['videoId'])):
	print str(100*(float(i)/float(len(data['videoId']))))[:5]+'%'
	try:
		# flag = 0
		# wordFreq = {}
		for words in combinations:
			definiteFraud = 0
			for sensitive in words:
				if sensitive in data['title'][i].lower():
					definiteFraud += 1
			if definiteFraud == len(words):
				if data['classification'][i]=='f':
					if str(words) in Graph['fraud']['title']:
						Graph['fraud']['title'][str(words)]+=1
					else:
						Graph['fraud']['title'][str(words)]=1

				elif data['classification'][i]=='b':
					if str(words) in Graph['benign']['title']:
						Graph['benign']['title'][str(words)]+=1
					else:
						Graph['benign']['title'][str(words)]=1
				# flag += 20
		for word in wordList:

			if word in data['title'][i].lower():
				if data['classification'][i]=='f':
					fwordCount+=1
					if word in Graph['fraud']['title']:  
						Graph['fraud']['title'][word]+=1
					else:
						Graph['fraud']['title'][word]=1

				elif data['classification'][i]=='b':
					bwordCount+=1
					if word in Graph['benign']['title']:
						Graph['benign']['title'][word]+=1
					else:
						Graph['benign']['title'][word]=1

			
	except Exception,e:
		print str(e) 
	try:
		
		for words in combinations:
			definiteFraud = 0
			for sensitive in words:
				if sensitive in data['description'][i].lower():
					definiteFraud += 1
			if definiteFraud == len(words):
				if data['classification'][i]=='f':
					if str(words) in Graph['fraud']['description']: 
						Graph['fraud']['description'][str(words)]+=1
					else:
						Graph['fraud']['description'][str(words)]=1

				elif data['classification'][i]=='b':
					if str(words) in Graph['benign']['description']: 
						Graph['benign']['description'][str(words)]+=1
					else:
						Graph['benign']['description'][str(words)]=1

		for word in wordList:
			
			if word in data['description'][i].lower():
				if data['classification'][i]=='f':
					fwordCount+=1
					if word in Graph['fraud']['description']: 
						Graph['fraud']['description'][word]+=1
					else:
						Graph['fraud']['description'][word]=1

				elif data['classification'][i]=='b':
					bwordCount+=1
					if word in Graph['benign']['description']: 
						Graph['benign']['description'][word]+=1
					else:
						Graph['benign']['description'][word]=1

				
	except Exception,e:
		print str(e)
	try:
		
		for words in combinations:
			definiteFraud = 0
			for sensitive in words:
				for tag in data['tags'][i]:
					if sensitive in tag.lower():
						definiteFraud += 1
						break
			if definiteFraud == len(words):
				if data['classification'][i]=='f':
					if str(words) in Graph['fraud']['tags']:
						Graph['fraud']['tags'][str(words)]+=1
					else:
						Graph['fraud']['tags'][str(words)]=1

				elif data['classification'][i]=='b':
					if str(words) in Graph['benign']['tags']: 
						Graph['benign']['tags'][str(words)]+=1
					else:
						Graph['benign']['tags'][str(words)]=1

		for word in wordList:
			for tag in data['tags'][i]:
				if word in tag.lower():
					if data['classification'][i]=='f':
						fwordCount+=1
						if word in Graph['fraud']['tags']:
							Graph['fraud']['tags'][word]+=1
							break
						else:
							Graph['fraud']['tags'][word]=1
							break

					elif data['classification'][i]=='b':
						bwordCount+=1
						if word in Graph['benign']['tags']: 
							Graph['benign']['tags'][word]+=1
							break
						else:
							Graph['benign']['tags'][word]=1
							break
					
	except Exception,e:
		print str(e)
	try:
		if len(data['linksDown'][i]):
			# linksDown+=len(data['linksDown'][i])
			if data['classification'][i]=='f':
				if 'linksDown' in Graph['fraud']: 
					Graph['fraud']['linksDown']+=len(data['linksDown'][i])
				else:
					Graph['fraud']['linksDown']=len(data['linksDown'][i])

			elif data['classification'][i]=='b':
				if 'linksDown' in Graph['benign']: 
					Graph['benign']['linksDown']+=len(data['linksDown'][i])
				else:
					Graph['benign']['linksDown']=len(data['linksDown'][i])
		if len(data['linksUp'][i]):
			# linksUp+=len(data['linksUp'][i])

			if data['classification'][i]=='f':
				if 'linksUp' in Graph['fraud']:
					Graph['fraud']['linksUp']+=len(data['linksUp'][i])
				else:
					Graph['fraud']['linksUp']=len(data['linksUp'][i])

			elif data['classification'][i]=='b':
				if 'linksUp' in Graph['benign']:
					Graph['benign']['linksUp']+=len(data['linksUp'][i])
				else: 
					Graph['benign']['linksUp']=len(data['linksUp'][i])

	except Exception,e:
		print str(e)

	try:
		if len(data['mcafeeHighRisk'][i]):
			if data['classification'][i]=='f':
				if 'mcafeeHighRisk' in Graph['fraud']:
					Graph['fraud']['mcafeeHighRisk']+=len(data['mcafeeHighRisk'][i])
				else:
					Graph['fraud']['mcafeeHighRisk']=len(data['mcafeeHighRisk'][i])
			elif data['classification'][i]=='b':
				if 'mcafeeHighRisk' in Graph['benign']:
					Graph['benign']['mcafeeHighRisk']+=len(data['mcafeeHighRisk'][i])
				else:
					Graph['benign']['mcafeeHighRisk']=len(data['mcafeeHighRisk'][i])
		if len(data['mcafeeMediumRisk'][i]):
			if data['classification'][i]=='f':
				if 'mcafeeMediumRisk' in Graph['fraud']:
					Graph['fraud']['mcafeeMediumRisk']+=len(data['mcafeeMediumRisk'][i])
				else:
					Graph['fraud']['mcafeeMediumRisk']=len(data['mcafeeMediumRisk'][i])
			elif data['classification'][i]=='b':
				if 'mcafeeMediumRisk' in Graph['benign']:
					Graph['benign']['mcafeeMediumRisk']+=len(data['mcafeeMediumRisk'][i])
				else:
					Graph['benign']['mcafeeMediumRisk']=len(data['mcafeeMediumRisk'][i])
		if len(data['mcafeeScannedLink'][i]):
			if data['classification'][i]=='f':
				if 'mcafeeScannedLink' in Graph['fraud']:
					Graph['fraud']['mcafeeScannedLink']+=len(data['mcafeeScannedLink'][i])
				else:
					Graph['fraud']['mcafeeScannedLink']=len(data['mcafeeScannedLink'][i])
			elif data['classification'][i]=='b':
				if 'mcafeeScannedLink' in Graph['benign']:
					Graph['benign']['mcafeeScannedLink']+=len(data['mcafeeScannedLink'][i])
				else:
					Graph['benign']['mcafeeScannedLink']=len(data['mcafeeScannedLink'][i])
		if len(data['mcafeeUnverified'][i]):
			if data['classification'][i]=='f':
				if 'mcafeeUnverified' in Graph['fraud']:
					Graph['fraud']['mcafeeUnverified']+=len(data['mcafeeUnverified'][i])
				else:
					Graph['fraud']['mcafeeUnverified']=len(data['mcafeeUnverified'][i])
			elif data['classification'][i]=='b':
				if 'mcafeeUnverified' in Graph['benign']:
					Graph['benign']['mcafeeUnverified']+=len(data['mcafeeUnverified'][i])
				else:
					Graph['benign']['mcafeeUnverified']=len(data['mcafeeUnverified'][i])
		# if len(data['maliciousLinks'][i]):
		# 	if data['classification'][i]=='f':
		# 		if 'maliciousLinks' in Graph['fraud']:
		# 			Graph['fraud']['maliciousLinks']+=len(data['maliciousLinks'][i])
		# 		else:
		# 			Graph['fraud']['maliciousLinks']=len(data['maliciousLinks'][i])
		# 	elif data['classification'][i]=='b':
		# 		if 'maliciousLinks' in Graph['benign']:
		# 			Graph['benign']['maliciousLinks']+=len(data['maliciousLinks'][i])
		# 		else:
		# 			Graph['benign']['maliciousLinks']=len(data['maliciousLinks'][i])
		# if len(data['virusTotalMcafeeCommonCount'][i]):
		# 	if data['classification'][i]=='f':
		# 		if 'virusTotalMcafeeCommonCount' in Graph['fraud']:
		# 			Graph['fraud']['virusTotalMcafeeCommonCount']+=len(data['virusTotalMcafeeCommonCount'][i])
		# 		else:
		# 			Graph['fraud']['virusTotalMcafeeCommonCount']=len(data['virusTotalMcafeeCommonCount'][i])
		# 	elif data['classification'][i]=='b':
		# 		if 'virusTotalMcafeeCommonCount' in Graph['benign']:
		# 			Graph['benign']['virusTotalMcafeeCommonCount']+=len(data['virusTotalMcafeeCommonCount'][i])
		# 		else:
		# 			Graph['benign']['virusTotalMcafeeCommonCount']=len(data['virusTotalMcafeeCommonCount'][i])


	except Exception,e:
		print str(e)
	
Graph['benign']['bwordCount']=bwordCount
Graph['fraud']['fwordCount']=fwordCount

with open('graphData.json','w') as f:
	json.dump(Graph,f)

