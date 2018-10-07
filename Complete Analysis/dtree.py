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

y_train =[] 

with open('doctree.txt','w') as f:
	t=""
	for i in range(len(data['videoId'])):
		if data['classification'][i] != 'Not classified':
			t+=data['title'][i].encode('ascii','ignore')+'\n'
			y_train.append(data['classification'][i])
	f.write(t)

with open('testData.txt','w') as f:
	t=""
	for i in range(len(data_test['videoId'])):
		t+=data_test['title'][i].encode('ascii','ignore')+'\n'
	f.write(t)

vectorizer = CountVectorizer()
with open('doctree.txt','r') as f:
	vectors = vectorizer.fit_transform(f)

X_train = vectors

with open('testData.txt','r') as f:
	vect = vectorizer.transform(f)

X_test = vect

y_test = []
for i in data_test['classification']:
	y_test.append(i.lower())
# data preprocessing

# example structure of data: title, tags, description, maliciousLinksCount e.g [[title, tags, description, 5]]

clf_entropy = DecisionTreeClassifier(criterion = "entropy", random_state = 100, min_samples_leaf=5)
clf_entropy.fit(X_train, y_train)

predictions = clf_entropy.predict(X_test)

print "accuracy: " + str(accuracy_score(y_test,predictions)*100) + "%"