import maliciousLinkCheck
import json 
import time

def scan():
	data = json.load(open('crawlerResult.json'))
	 
	uniqueLinks=[] 
	for i in range(len(data['linksUp'])):
		for link in data['linksUp'][i]:
			if link not in uniqueLinks:
				uniqueLinks.append(link)
	API_KEYS = [
				'2d6412a6aa8141fa09989a8dfa82c5cb5b2076684cb42c0d3a2593339dd604b3',
				'ce2ef7700bb39560f306cc04374bdacf9b0c2c9bb1e0ab7c9e3e2967a7e72317',
				'c1bda5b057861a6283570f01e1f62e13e6b43096374a01e410f4af5e35577d9f',
				'f8141d6cc0aa12c03e004c52fec0809e8846ba6b7e18e6cc68c2fb92aeb09b1b',
				'ee3ce82e29f4f8c03b324a9ff6dc65a341ffcd7f6835a3d6a1a1ac6a80a8ce3f',
				'94db0a4b894a22d5ab60a9ee58c76221e55e62339e9e50fdeb457da183194a02',
				'f6dedd93fe91ea4b7a2ca87fb32ceb923d86c95bd6997fe371ff2eb7a379f2c1',
				'34cc1a775a7194f0dbdd9af2130c790649c9f5899d217829f8fb06bfbd000c92',
				'1b82c868e35890b4b797d2b9eb9a968af753535c0c520ab9129cdc3c89a7c389',
				'f852748426b09a1b34e4f15cfe6ab3e29eaa647f315a2a1cb6210d449e8b647a',
				'9b9d5140cbfd0f941486f0c6fa6342a7bee3812a315252d521535b9f2e9be9e0',
				'6cd99eddeb1ac0ded05dab5955d088d5db7637b7b969b28788c6c2a6f007bf93'
			]

	parts = len(uniqueLinks)/len(API_KEYS)
	count = 0
	start = [parts*0,parts*1,parts*2,parts*3,parts*4,parts*5,parts*6,parts*7,parts*8,parts*9,parts*10,parts*11]
	loopCheck = parts/4
	progress = 0
	while True:
		for i in range(12):
			try:	
				maliciousLinkCheck.submitURL(uniqueLinks[(4*count)+start[i]:(4*(count+1))+start[i]],API_KEYS[i])
				progress += 4
			except:
				i-=1
				continue
		print str(100*float(progress)/len(uniqueLinks))[:5]+'%'
		time.sleep(60)
		count = count+1
		if count > loopCheck-1:
			break

	for i in range(12):
		try:
			if i == 11:
				remainingLinks = 0
				for link in uniqueLinks[start[i]+(4*count):]:
					maliciousLinkCheck.submitURL(link,API_KEYS[remainingLinks])
					remainingLinks+=1
			else:
				maliciousLinkCheck.submitURL(uniqueLinks[start[i]+(4*(count)):start[i+1]],API_KEYS[i])
		except:
			i-=1

	print "All Urls Submitted to VirusTotal...."
	print "Retrieving Reports...."

	count = 0
	index = 0
	requestResults = {}
	while True:
		for i in range(12):
			requestResults[index] = maliciousLinkCheck.getReports(uniqueLinks[(4*count)+start[i]:(4*(count+1))+start[i]],API_KEYS[i])
			with open('URL_VirusTotal_Results.json','w') as f:
					json.dump(requestResults,f)
			index+=1
		time.sleep(60)
		count = count+1
		if count > loopCheck-1:
			break

	for i in range(12):
		if i == 11:
			remainingLinks = 0
			for link in uniqueLinks[start[i]+(4*count):]:
				requestResults[index] = maliciousLinkCheck.getReports(link,API_KEYS[remainingLinks])
				with open('URL_VirusTotal_Results.json','w') as f:
					json.dump(requestResults,f)
				print "Done"
				index+=1
				remainingLinks+=1
		else:
			requestResults[index] = maliciousLinkCheck.getReports(uniqueLinks[start[i]+(4*(count)):start[i+1]],API_KEYS[i])
			with open('URL_VirusTotal_Results.json','w') as f:
					json.dump(requestResults,f)
			index+=1
