import requests
import json

# submitResponse=[]
def submitURL(urlList,API_KEY):
	params = {'apikey': API_KEY, 'url':urlList[0] + '\n'}
	for url in urlList[1:]:
		params['url'] += url+'\n'
	params['url'] = params['url'][:-1]
	response = requests.post('https://www.virustotal.com/vtapi/v2/url/scan', data=params)

def getReports(urlList,API_KEY):
	headers = {
		"Accept-Encoding": "gzip, deflate",
		"User-Agent" : "gzip,  My Python requests library example client or username"
	}
	params = {'apikey': API_KEY, 'resource':urlList[0] + '\n'}
	for url in urlList[1:]:
		params['resource'] += url+'\n'
	params['resource'] = params['resource'][:-1]
	response = requests.get('https://www.virustotal.com/vtapi/v2/url/report', params=params,headers=headers)
	# reportResponse[index] = response.json()
	return response.json()

# with open('URL_VirusTotal_Results.json','w') as f:
# 	json.dump(reportResponse,f)