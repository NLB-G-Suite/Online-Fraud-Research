import json
import numpy as np
import pandas as pd
from nltk.stem.porter import PorterStemmer
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn import tree
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
from stop_words import get_stop_words
import csv
import nltk
from nltk.tokenize import RegexpTokenizer
import re

data = json.load(open('dataset.json'))
data_test = json.load(open('data_test.json'))
dataBenign= json.load(open('benignData.json'))
videos = []
test = []

index=[]
highRisk = {}
mediumRisk = {}

for i in range(len(data_test['videoId'])):
	if data_test['videoId'][i][32:]=='https://www.youtube.com/watch?v=F1-poGrDhCI':
		# print 'h'
		print data_test['classification'][i]
for i in range(len(data_test['videoId'])):
	for j in range(len(data['videoId'])):
		if data_test['videoId'][i][64:] == data['videoId'][j]:
			highRisk[i] = data['mcafeeHighRisk'][j]
			mediumRisk[i] = data['mcafeeMediumRisk'][j]
			break

data_test['mcafeeHighRisk'] = highRisk
data_test['mcafeeMediumRisk'] = mediumRisk

en_stop = get_stop_words('en')

y=[]
for i in range(len(data['videoId'])):
	if data['classification'][i] != 'Not classified':
		try:
			videos.append(data['title'][i].encode('ascii','ignore')+data['description'][i].encode('ascii','ignore')+str(data['tags'][i]))
			# if len(data['mcafeeHighRisk'][i]):
			# 	videos[-1] += ' '+str(['HighRisk ' for g in data['mcafeeHighRisk'][i]])
			# if len(data['mcafeeMediumRisk'][i]):
			# 	videos[-1] += ' '+str(['MediumRisk ' for g in data['mcafeeMediumRisk'][i]])
			# if len(data['linksDown'][i]):
			# 	videos[-1] += ' '+str(['linkDown ' for g in data['linksDown'][i]])
			index.append(i)
			y.append(data['classification'][i].lower())
		except:
			videos.append(data['title'][i].encode('ascii','ignore')+str(data['tags'][i]))
			# if len(data['mcafeeHighRisk'][i]):
			# 	videos[-1] += ' '+str(['HighRisk ' for g in data['mcafeeHighRisk'][i]])
			# if len(data['mcafeeMediumRisk'][i]):
			# 	videos[-1] += ' '+str(['MediumRisk ' for g in data['mcafeeMediumRisk'][i]])
			# if len(data['linksDown'][i]):
			# 	videos[-1] += ' '+str(['linkDown ' for g in data['linksDown'][i]])
			index.append(i)		
			y.append(data['classification'][i].lower())
for i in range(len(data_test['videoId'])):
	try:
		videos.append(data_test['title'][i].encode('ascii','ignore')+data_test['description'][i].encode('ascii','ignore')+str(data_test['tags'][i]))
		# if len(data_test['mcafeeHighRisk'][i]):
		# 	videos[-1] += ' '+str(['HighRisk ' for g in data_test['mcafeeHighRisk'][i]])
		# if len(data_test['mcafeeMediumRisk'][i]):
		# 	videos[-1] += ' '+str(['MediumRisk ' for g in data_test['mcafeeMediumRisk'][i]])
		# if len(data_test['linksDown'][i]):
		# 	videos[-1] += ' '+str(['linkDown ' for g in data_test['linksDown'][i]])
		index.append(i+len(data['videoId']))
		y.append(data_test['classification'][i].lower())	
	except:
		videos.append(data_test['title'][i].encode('ascii','ignore')+str(data_test['tags'][i]))
		# if len(data_test['mcafeeHighRisk'][i]):
		# 	videos[-1] += ' '+str(['HighRisk ' for g in data_test['mcafeeHighRisk'][i]])
		# if len(data_test['mcafeeMediumRisk'][i]):
		# 	videos[-1] += ' '+str(['MediumRisk ' for g in data_test['mcafeeMediumRisk'][i]])
		# if len(data_test['linksDown'][i]):
		# 	videos[-1] += ' '+str(['linkDown ' for g in data_test['linksDown'][i]])
		index.append(i+len(data['videoId']))
		y.append(data_test['classification'][i].lower())

for i in range(len(dataBenign['videoId'])):
	try:
		videos.append(dataBenign['title'][i].encode('ascii','ignore')+dataBenign['description'][i].encode('ascii','ignore')+str(dataBenign['tags'][i]))
		# if len(dataBenign['mcafeeHighRisk'][i]):
		# 	videos[-1] += ' '+str(['HighRisk ' for g in dataBenign['mcafeeHighRisk'][i]])
		# if len(dataBenign['mcafeeMediumRisk'][i]):
		# 	videos[-1] += ' '+str(['MediumRisk ' for g in dataBenign['mcafeeMediumRisk'][i]])
		# if len(dataBenign['linksDown'][i]):
		# 	videos[-1] += ' '+str(['linkDown ' for g in dataBenign['linksDown'][i]])
		index.append(i+len(data['videoId'])+len(data_test['videoId']))
		y.append(dataBenign['classification'][i].lower())	
	except:
		videos.append(dataBenign['title'][i].encode('ascii','ignore')+str(dataBenign['tags'][i]))
		# if len(dataBenign['mcafeeHighRisk'][i]):
		# 	videos[-1] += ' '+str(['HighRisk ' for g in dataBenign['mcafeeHighRisk'][i]])
		# if len(dataBenign['mcafeeMediumRisk'][i]):
		# 	videos[-1] += ' '+str(['MediumRisk ' for g in dataBenign['mcafeeMediumRisk'][i]])
		# if len(dataBenign['linksDown'][i]):
		# 	videos[-1] += ' '+str(['linkDown ' for g in dataBenign['linksDown'][i]])
		index.append(i+len(data['videoId'])+len(data_test['videoId']))
		y.append(dataBenign['classification'][i].lower())

tokenizer = RegexpTokenizer(r'\w+')
p_stemmer = PorterStemmer()
en_stop = get_stop_words('en')
# nltk.download('averaged_perceptron_tagger')

for i in range(len(videos)):				
	raw = re.sub(r'[0-9]+','',videos[i].lower())
	tokens = tokenizer.tokenize(raw)
	# remove stop words from tokens
	stopped_tokens = [j for j in tokens if not j in en_stop]
	# stem tokens
	stemmed_tokens = [p_stemmer.stem(j) for j in stopped_tokens]
	# add tokens to list
	videos[i] = stemmed_tokens
	t = ''
	for k in videos[i]:
		t += k + ' '
	t = t.replace('www','')
	t = t.replace('http','')
	t = t.replace('https','')
	t = t.replace('com','')
	t += "    " + str(index[i])
	videos[i] = t 


xTrain1, xTest1, y_train, y_test = train_test_split(videos, y, test_size=0.3, random_state=100)
# y_train=[]
# y_train=y
# # xTest1=[]
# len1=0
# for i in range(len(dataCrypto['videoId'])):
# 	len1+=1
# 	try:
# 		xTest1.append(dataCrypto['title'][i].encode('ascii','ignore')+dataCrypto['description'][i].encode('ascii','ignore')+str(dataCrypto['tags'][i]))
# 	except:
# 		xTest1.append(dataCrypto['title'][i].encode('ascii','ignore')+str(dataCrypto['tags'][i]))
# len2=0
# for i in range(len(dataAds['videoId'])):
# 	len2+=1
# 	try:
# 		xTest1.append(dataAds['title'][i].encode('ascii','ignore')+dataAds['description'][i].encode('ascii','ignore')+str(dataAds['tags'][i]))
# 	except:
# 		xTest1.append(dataAds['title'][i].encode('ascii','ignore')+str(dataAds['tags'][i]))
# len3=0
# for i in range(len(dataStock['videoId'])):
# 	len3+=1
# 	try:
# 		xTest1.append(dataStock['title'][i].encode('ascii','ignore')+dataStock['description'][i].encode('ascii','ignore')+str(dataStock['tags'][i]))
# 	except:
# 		xTest1.append(dataStock['title'][i].encode('ascii','ignore')+str(dataStock['tags'][i]))

vectorizer = CountVectorizer()
xTrain2 = []
# xTrain2 = xTrain1
for i in range(len(xTrain1)):
	xTrain2.append(xTrain1[i])
for i in range(len(xTrain1)):
	xTrain1[i] = xTrain1[i][:-4]
xTrain1 = vectorizer.fit_transform(xTrain1)


# xTrain1 = vectorizer.fit_transform(videos)


xTest2 = []
for i in range(len(xTest1)):
	xTest2.append(xTest1[i])
for i in range(len(xTest1)):
	xTest1[i] = xTest1[i][:-4]
xTest1 = vectorizer.transform(xTest1)
# data preprocessing

# example structure of data: title, tags, description, maliciousLinksCount e.g [[title, tags, description, 5]]
clf_entropy = RandomForestClassifier(n_estimators=10000,criterion='gini')
clf_entropy.fit(xTrain1,y_train)
# est = clf_entropy.estimators_[99]
predictions = clf_entropy.predict(xTest1)
print "accuracy: " + str(accuracy_score(y_test,predictions)*100) + "%"

wrongPred = []
for i in range(len(predictions)):
	if predictions[i]!=y_test[i]:
		if int(xTest2[i][-4:]) < len(data['videoId']):
			# print ['d'+xTest2[i][-4:],data['videoId'][int(xTest2[i][-4:])],predictions[i],y_test[i],data['classification'][int(xTest2[i][-4:])]]
			wrongPred.append(['d'+xTest2[i][-4:],data['videoId'][int(xTest2[i][-4:])],predictions[i],y_test[i]])
		elif int(xTest2[i][-4:]) < (len(data['videoId'])+len(data_test['videoId'])):
			# print ['dt'+xTest2[i][-4:],data_test['videoId'][int(xTest2[i][-4:])-len(data['videoId'])][32:],predictions[i],y_test[i],data_test['classification'][int(xTest2[i][-4:])-len(data['videoId'])]]
			wrongPred.append(['dt'+xTest2[i][-4:],data_test['videoId'][int(xTest2[i][-4:])-len(data['videoId'])][32:],predictions[i],y_test[i]])			
		else:
			# print ['db'+xTest2[i][-4:],dataBenign['videoId'][int(xTest2[i][-4:])-(len(data['videoId'])+len(data_test['videoId']))][32:],predictions[i],y_test[i],dataBenign['classification'][int(xTest2[i][-4:])-(len(data['videoId'])+len(data_test['videoId']))]]
			wrongPred.append(['db'+xTest2[i][-4:],dataBenign['videoId'][int(xTest2[i][-4:])-(len(data['videoId'])+len(data_test['videoId']))][32:],predictions[i],y_test[i]])			

		# except:
		# 	print 'EXCPETION'
		# 	continue
			# print i,xTest2[i]
print wrongPred


# wrongPred = []
# for i in range(len(predictions)):
# 	if i<len1:
# 		wrongPred.append(['https://www.youtube.com/watch?v='+dataCrypto['videoId'][i],predictions[i]])
# 		# dataCrypto['classification'][i]=predictions[i]

# 	elif i<len1+len2:
# 		wrongPred.append(['https://www.youtube.com/watch?v='+dataAds['videoId'][i-len1],predictions[i]])
# 		# dataAds['classification'][i]=predictions[i]

# 	else:
# 		wrongPred.append(['https://www.youtube.com/watch?v='+dataStock['videoId'][i-(len1+len2)],predictions[i]])
# 		# dataStock['classification'][i]=predictions[i]

# dataAds['classification']=[]
# dataAds['category']=[]

# for i in range(len(dataAds['videoId'])):
# 	dataAds['videoId'][i]='https://www.youtube.com/watch?v='+dataAds['videoId'][i]
# 	dataAds['classification'].append('b')
# 	with open ('categorylist.txt','r') as file:
# 			for line in file:
# 				if dataAds['categoryId'][i] in line:
# 					dataAds['category'].append(line[4:])
# 					print [dataAds['category'][i],dataAds['categoryId'][i],line[0:3]]
# 					break
		
	
# for i in range(len(dataStock['videoId'])):
# 	dataAds['videoId'].append('https://www.youtube.com/watch?v='+dataStock['videoId'][i])
# 	dataAds['title'].append(dataStock['title'][i])
# 	dataAds['channelId'].append(dataStock['channelId'][i])
# 	with open ('categorylist.txt','r') as file:
# 			for line in file:
# 				if dataStock['categoryId'][i] in line:
# 					dataAds['category'].append(line[4:])
	
# 	dataAds['classification'].append('b')
# 	dataAds['viewCount'].append(dataStock['viewCount'][i])
# 	dataAds['commentCount'].append(dataStock['commentCount'][i])
# 	dataAds['comments'].append(dataStock['comments'][i])
# 	dataAds['tags'].append(dataStock['tags'][i])
# 	dataAds['description'].append(dataStock['description'][i])

	
# for i in range(len(dataCrypto['videoId'])):
# 	dataAds['videoId'].append('https://www.youtube.com/watch?v='+dataCrypto['videoId'][i])
# 	dataAds['title'].append(dataCrypto['title'][i])
# 	dataAds['channelId'].append(dataCrypto['channelId'][i])
# 	with open ('categorylist.txt','r') as file:
# 			for line in file:
# 				if dataCrypto['categoryId'][i] in line:
# 					dataAds['category'].append(line[4:])
	
# 	dataAds['classification'].append('b')
# 	dataAds['viewCount'].append(dataCrypto['viewCount'][i])
# 	dataAds['commentCount'].append(dataCrypto['commentCount'][i])
# 	dataAds['comments'].append(dataCrypto['comments'][i])
# 	dataAds['tags'].append(dataCrypto['tags'][i])
# 	dataAds['description'].append(dataCrypto['description'][i])

# with open('benignData.json','w') as f:
# 	json.dump(dataAds,f)

	
		
# print len(wrongPred)

