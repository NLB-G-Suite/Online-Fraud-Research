import json
import urllib2
import requests
from bs4 import BeautifulSoup
import socket

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'}

urls = json.load(open('domainList.json'))
signup = ['register','join','signup','sign-up','sign up','start']
completeData = json.load(open('formData.json'))
errorUrls = []

def getPage(url):
	try:
		html=requests.get(url,headers=headers).text
	except Exception,e:
		print "GET Page Error "+str(e)
	soup = BeautifulSoup(html)
	divList = soup.findAll('a')
	for div in divList:
		for word in signup:
			if word.lower() in div.text.lower():
				try:
					return [div['href'],url]
				except:
					return ['lol',url]

def getForm(url):
	print url
	data = []
	whatWorks = ''
	try:
		try:
			html=requests.get(url[0],headers=headers).text
			whatWorks = url[0]
		except:
			html=requests.get(url[1]+url[0],headers=headers).text
			whatWorks = url[1]+url[0]
	except:
		html=requests.get(url[1],headers=headers).text
		whatWorks = url[1]
	soup = BeautifulSoup(html)
	formList = soup.findAll('label')
	for div in formList:
		try:
			data.append(div.text)
		except:
			continue
	if len(formList)==0:
		formList = soup.findAll('input')
		for div in formList:
			try:
				data.append(div['name'])
			except:
				continue		
	completeData[whatWorks] = data
	# print data
count = 0
for url in urls:
	print url
	if url in completeData:
		continue
	print 'Percentage Complete:',str(100*float(count)/len(urls))[:5]
	try:
# url='https://www.tubetycoon.com/optin-25689503'
		getForm(getPage(url))
	except Exception,e:
		print str(e)
		errorUrls.append(url)
	count += 1
 
with open('formData.json','w') as f:
	json.dump(completeData,f)

with open('errorUrls.json','w') as f:
	json.dump(errorUrls,f)
