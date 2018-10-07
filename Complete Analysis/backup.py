import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn import tree
from sklearn.feature_extraction.text import CountVectorizer

data = json.load(open('linkStatusBuffer(1).json'))
data_test = pd.read_csv('unclassifiedScores.csv')

videos = []

y_train =[] 

with open('descTree.txt','w') as f:
	t=""
	for i in range(len(data['videoId'])):
		if data['classification'][i] != 'Not classified':
			try:
				t+=(str(data['description'][i])).replace('\n',' ').encode('ascii','ignore')+'\n'
			except:
				t+='No description\n'
				continue
	f.write(t)

with open('descTest.txt','w') as f:
	t=""
	for i in range(len(data_test['videoId'])):
		try:
			t+=(str(data_test['description'][i])).replace('\n',' ').encode('ascii','ignore')+'\n'
		except:
			t+='No description\n'
			continue
	f.write(t)

with open('titleTree.txt','w') as f:
	t=""
	for i in range(len(data['videoId'])):
		if data['classification'][i] != 'Not classified':
			t+=data['title'][i].encode('ascii','ignore')+'\n'
			y_train.append(data['classification'][i])
	f.write(t)

with open('titleTest.txt','w') as f:
	t=""
	for i in range(len(data_test['videoId'])):
		t+=data_test['title'][i].encode('ascii','ignore')+'\n'
	f.write(t)

with open('tagsTree.txt','w') as f:
	t=""
	for i in range(len(data['videoId'])):
		if data['classification'][i] != 'Not classified':
			t+=str(data['tags'][i]).encode('ascii','ignore')+'\n'
	f.write(t)

with open('tagsTest.txt','w') as f:
	t=""
	for i in range(len(data_test['videoId'])):
		t+=str(data_test['tags'][i]).encode('ascii','ignore')+'\n'
	f.write(t)


vectorizer = CountVectorizer()
with open('tagsTree.txt','r') as f:
	xTrainTags = vectorizer.fit_transform(f)
with open('descTree.txt','r') as f:
	xTrainDesc = vectorizer.fit_transform(f)
with open('titleTree.txt','r') as f:
	xTrainTitle = vectorizer.fit_transform(f)

with open('descTest.txt','r') as f:
	xTestDesc = vectorizer.transform(f)
with open('titleTest.txt','r') as f:
	xTestTitle = vectorizer.transform(f)
with open('tagsTest.txt','r') as f:
	xTestTags = vectorizer.transform(f)

y_test = []
for i in data_test['classification']:
	y_test.append(i.lower())

print len(y_train)
# print X_train
# data preprocessing

# example structure of data: title, tags, description, maliciousLinksCount e.g [[title, tags, description, 5]]

clf_entropy = DecisionTreeClassifier(criterion = "entropy", random_state = 100, min_samples_leaf=5)
# x_train = np.asarray([xTrainDesc,xTrainTitle,xTrainTags])
clf_entropy.fit(xTrainTitle, y_train)

predictions = clf_entropy.predict(xTestTitle)

print "accuracy: " + str(accuracy_score(y_test,predictions)*100) + "%"