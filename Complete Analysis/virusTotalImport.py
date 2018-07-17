import json 

data=json.load(open('linkStatusBuffer.json'))
virusTotal=json.load(open('URL_VirusTotal_Results.json'))

url={}
for list in virusTotal.values():
	for dictionary in list:
		try:
			malwareType = {}
			check = 0
			for site in dictionary["scans"].keys():
				if dictionary["scans"][site]["detected"]==True and not('amazon.com' in dictionary["url"] or 'amzn.' in dictionary["url"]  or "adf.ly" in dictionary["url"]):
					malwareType[site]=dictionary["scans"][site]["result"]
					check = 1
			if check == 0:
				url[dictionary["resource"]] = {'result':'clean site'}
			else:
				url[dictionary["resource"]] = malwareType
		except KeyError:
			url[dictionary["resource"]] = {}
		except Exception,e:
			print str(e)
total = []
for i in range(len(data['videoId'])):
	maliciousLinks={}
	check=0
	for link in data['linksUp'][i]:
		if link in url:
			maliciousLinks[link] = url[link]
		else:
			maliciousLinks[link] = {'result':'unknown'}
	total.append(maliciousLinks)
data['scannedLink'] = total

with open('linkStatusBuffer.json','w') as f:
	json.dump(data,f)