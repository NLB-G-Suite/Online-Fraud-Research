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

videos = []
test = []

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
			if len(data['mcafeeHighRisk'][i]):
				videos[-1] += ' '+str(['HighRisk ' for g in data['mcafeeHighRisk'][i]])
			if len(data['mcafeeMediumRisk'][i]):
				videos[-1] += ' '+str(['MediumRisk ' for g in data['mcafeeMediumRisk'][i]])
			if len(data['linksDown'][i]):
				videos[-1] += ' '+str(['linkDown ' for g in data['linksDown'][i]])
			y.append(data['classification'][i].lower())
		except:
			videos.append(data['title'][i].encode('ascii','ignore')+str(data['tags'][i]))
			if len(data['mcafeeHighRisk'][i]):
				videos[-1] += ' '+str(['HighRisk ' for g in data['mcafeeHighRisk'][i]])
			if len(data['mcafeeMediumRisk'][i]):
				videos[-1] += ' '+str(['MediumRisk ' for g in data['mcafeeMediumRisk'][i]])
			if len(data['linksDown'][i]):
				videos[-1] += ' '+str(['linkDown ' for g in data['linksDown'][i]])		
			y.append(data['classification'][i].lower())
for i in range(len(data_test['videoId'])):
	try:
		videos.append(data_test['title'][i].encode('ascii','ignore')+data_test['description'][i].encode('ascii','ignore')+str(data_test['tags'][i]))
		if len(data_test['mcafeeHighRisk'][i]):
			videos[-1] += ' '+str(['HighRisk ' for g in data_test['mcafeeHighRisk'][i]])
		if len(data_test['mcafeeMediumRisk'][i]):
			videos[-1] += ' '+str(['MediumRisk ' for g in data_test['mcafeeMediumRisk'][i]])
		if len(data_test['linksDown'][i]):
			videos[-1] += ' '+str(['linkDown ' for g in data_test['linksDown'][i]])
		y.append(data_test['classification'][i].lower())	
	except:
		videos.append(data_test['title'][i].encode('ascii','ignore')+str(data_test['tags'][i]))
		if len(data_test['mcafeeHighRisk'][i]):
			videos[-1] += ' '+str(['HighRisk ' for g in data_test['mcafeeHighRisk'][i]])
		if len(data_test['mcafeeMediumRisk'][i]):
			videos[-1] += ' '+str(['MediumRisk ' for g in data_test['mcafeeMediumRisk'][i]])
		if len(data_test['linksDown'][i]):
			videos[-1] += ' '+str(['linkDown ' for g in data_test['linksDown'][i]])
		y.append(data_test['classification'][i].lower())
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
	# stemmed_tokens = nltk.pos_tag(stemmed_tokens)
	# temp = []
	# for t in stemmed_tokens:
	# 	if t[1][0] == 'N':
	# 		temp.append(t[0])
	# 	elif t[1][0] == 'V':
	# 		temp.append(t[0])
	# 	elif t[1][0] == 'X':
	# 		temp.append(t[0])
	# 	elif t[1][0] == 'A':
	# 		temp.append(t[0])
	videos[i] = stemmed_tokens
	t = ''
	for k in videos[i]:
		t += k + ' '
	t = t.replace('www','')
	t = t.replace('http','')
	t = t.replace('https','')
	t = t.replace('com','')
	# if t.find(' click ') != -1:
	# 	t += 'click ' 
	# 	t += 'click '
	# if t.find(' ad') != -1:
	# 	t += 'ad '
	# 	t += 'ad '
	t += "   " + str(i)
	videos[i] = t 

# y = [i.lower() for i in data['classification'] if i != 'Not classified']
# for i in data_test['classification']:
# 	y.append(i.lower())

xTrain1, xTest1, y_train, y_test = train_test_split(videos, y, test_size=0.1, random_state=100)

vectorizer = CountVectorizer()
xTrain2 = []
xTrain2 = xTrain1
for i in range(len(xTrain1)):
	xTrain1[i] = xTrain1[i][:-3]
xTrain1 = vectorizer.fit_transform(xTrain1)


xTest2 = []
for i in range(len(xTest1)):
	xTest2.append(xTest1[i])
for i in range(len(xTest1)):
	xTest1[i] = xTest1[i][:-3]
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
		# try:
			# print xTest2[i]
		if int(xTest2[i][-3:]) < 510:
			wrongPred.append([data['videoId'][int(xTest2[i][-3:])][32:],predictions[i],y_test[i]])
		else:
			wrongPred.append([data_test['videoId'][int(xTest2[i][-3:])-510][32:],predictions[i],y_test[i]])			
		# except:
		# 	print 'EXCPETION'
		# 	continue
			# print i,xTest2[i]
print wrongPred

# my_matrix = metrics.confusion_matrix(y_test,predictions)
# print my_matrix

# tree.export_graphviz(est,out_file='dtree.dot',feature_names=vectorizer.get_feature_names())
