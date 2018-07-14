import requests
import time


submitResponse=[]
def submitURL(urlList,API_KEY):
	for i in range(len(urlList)):	
		params = {'apikey': API_KEY, 'url':urlList[i] + '\n' + urlList[i+1] + '\n' + urlList[i+2] + '\n' + urlList[i+3]}
		response = requests.post('https://www.virustotal.com/vtapi/v2/url/scan', data=params)
		print str(i+4/float(len(urlList))*100)[:4]+'%'
		submitResponse.append(response.json())
		time.sleep(60)
		i = i + 4

reportResponse=[]
def getReports(urlList,API_KEY):
	headers = {
		"Accept-Encoding": "gzip, deflate",
		"User-Agent" : "gzip,  My Python requests library example client or username"
	}
	for i in range(len(urlList)):	
		params = {'apikey': API_KEY, 'url':urlList[i] + '\n' + urlList[i+1] + '\n' + urlList[i+2] + '\n' + urlList[i+3]}
		response = requests.post('https://www.virustotal.com/vtapi/v2/url/scan', data=params)
		print str(i+4/float(len(urlList))*100)[:4]+'%'
		reportResponse.append(response.json())
		json_response = response.json()
		#store json in file
		time.sleep(60)
		i = i + 4
 