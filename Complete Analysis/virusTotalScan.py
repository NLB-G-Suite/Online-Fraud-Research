import maliciousLinkCheck
import json 

data = json.load(open('linkStatus.json'))
 
uniqueLinks=[] 
for i in range(len(data['linksUp'])):
	for link in data['linksUp'][i]:
		if link not in uniqueLinks:
			uniqueLinks.append(link)
API_KEYS=[]

parts=len(uniqueLinks)/len(API_KEYS)
count=0
for API_KEY in API_KEYS:
	if count+1!=len(API_KEYS):
		maliciousLinkCheck.submitURL(uniqueLinks[count*parts:count+1*parts],API_KEY)
		count=count+1
maliciousLinkCheck.submitURL(uniqueLinks[(len(API_KEYS)-1)*parts:],API_KEY)
print "All Urls Submitted to VirusTotal...."
print "Retrieving Reports...."
count=0
for API_KEY in API_KEYS:
	if count+1!=len(API_KEYS):
		maliciousLinkCheck.getReports(uniqueLinks[count*parts:count+1*parts],API_KEY)
		count=count+1
maliciousLinkCheck.getReports(uniqueLinks[(len(API_KEYS)-1)*parts:],API_KEY)
print "Done"