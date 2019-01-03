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

data1 = json.load(open('t1.json'))
data2 = json.load(open('t2.json'))
data3 = json.load(open('t3.json'))


description=[]
tags=[]
channelId=[]
channelTitle=[]
categoryId=[]
title=[]
videoId=[]
viewCount=[]
commentCount=[] 
comments=[]

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
			index.append(i)
			y.append(data['classification'][i].lower())
		except:
			videos.append(data['title'][i].encode('ascii','ignore')+str(data['tags'][i]))
			index.append(i)		
			y.append(data['classification'][i].lower())
for i in range(len(data_test['videoId'])):
	try:
		videos.append(data_test['title'][i].encode('ascii','ignore')+data_test['description'][i].encode('ascii','ignore')+str(data_test['tags'][i]))
		index.append(i+len(data['videoId']))
		y.append(data_test['classification'][i].lower())	
	except:
		videos.append(data_test['title'][i].encode('ascii','ignore')+str(data_test['tags'][i]))
		index.append(i+len(data['videoId']))
		y.append(data_test['classification'][i].lower())

for i in range(len(dataBenign['videoId'])):
	try:
		videos.append(dataBenign['title'][i].encode('ascii','ignore')+dataBenign['description'][i].encode('ascii','ignore')+str(dataBenign['tags'][i]))
		index.append(i+len(data['videoId'])+len(data_test['videoId']))
		y.append(dataBenign['classification'][i].lower())	
	except:
		videos.append(dataBenign['title'][i].encode('ascii','ignore')+str(dataBenign['tags'][i]))
		index.append(i+len(data['videoId'])+len(data_test['videoId']))
		y.append(dataBenign['classification'][i].lower())

tokenizer = RegexpTokenizer(r'\w+')
p_stemmer = PorterStemmer()
en_stop = get_stop_words('en')


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
	# t += "    " + str(index[i])
	videos[i] = t 


y_train=[]
y_train=y


vectorizer = CountVectorizer()
xTrain1 = vectorizer.fit_transform(videos)


#predClass=[]
unique_fraud=[]
unique_benign=[]
xTest1=[]
xTest2=[]
xTest3=[]

# 	totalVideos=0
b=0
f=0

	
for i in range(len(data1['videoId'])):
	for c in range(len(data1['linkContent'][i])):
		try:
			xTest1.append(data1['linkContent'][i][c])
		except:
			xTest1.append('No link content')

for i in range(len(data2['videoId'])):
	for c in range(len(data2['linkContent'][i])):
		try:
			xTest2.append(data2['linkContent'][i][c])
		except:
			xTest2.append('No link content')

for i in range(len(data3['videoId'])):
	for c in range(len(data3['linkContent'][i])):
		try:
			xTest3.append(data3['linkContent'][i][c])
		except:
			xTest3.append('No link content')

xTest1 = vectorizer.transform(xTest1)
xTest2 = vectorizer.transform(xTest2)
xTest3 = vectorizer.transform(xTest3)

# example structure of data: title, tags, description, maliciousLinksCount e.g [[title, tags, description, 5]]
clf_entropy = RandomForestClassifier(n_estimators=10000,criterion='gini')
clf_entropy.fit(xTrain1,y_train)
prediction1 = clf_entropy.predict(xTest1)
prediction2 = clf_entropy.predict(xTest2)
prediction3 = clf_entropy.predict(xTest3)

videoLink1=[]
videoLink2=[]
videoLink3=[]

for i in range(len(data1['videoId'])):
	for c in range(len(data1['linksUp'][i])):
		videoLink1.append(data1['linksUp'][i][c])
for i in range(len(prediction1)):
	# predClass.append(predictions[i])
	if prediction1[i]=='f':
		unique_fraud.append(videoLink1[i])
		f+=1
	elif prediction1[i]=='b':
		unique_benign.append(videoLink1[i])
		b+=1

for i in range(len(data2['videoId'])):
	for c in range(len(data2['linksUp'][i])):
		videoLink2.append(data2['linksUp'][i][c])

for i in range(len(prediction2)):
	# predClass.append(predictions[i])
	if prediction2[i]=='f':
		unique_fraud.append(videoLink2[i])
		f+=1
	elif prediction2[i]=='b':
		unique_benign.append(videoLink2[i])
		b+=1

for i in range(len(data3['videoId'])):
	for c in range(len(data3['linksUp'][i])):
		videoLink3.append(data3['linksUp'][i][c])
for i in range(len(prediction3)):
	# predClass.append(predictions[i])
	if prediction3[i]=='f':
		unique_fraud.append(videoLink3[i])
		f+=1
	elif prediction3[i]=='b':
		unique_benign.append(videoLink3[i])
		b+=1
# chanVideos[channel]['predClass']=predClass

with open('classifyDomains.json', 'w') as fp:
    json.dump(unique_fraud,fp)
