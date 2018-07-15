import json
import safebrowsing

data = json.load(open('linkStatus.json'))

uniqueLinks = []
for i in range(len(data['linksUp'])):
	for link in data['linksUp'][i]:
		if link not in uniqueLinks:
			uniqueLinks.append(link)
 
apikey = 'AIzaSyAbyb2yj9r9N0mSF7LdWPZgLiwguDiyN48'
sb = safebrowsing.LookupAPI(apikey)
resp = sb.threat_matches_find(uniqueLinks) 
print resp
