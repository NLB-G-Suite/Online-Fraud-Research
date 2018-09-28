import numpy as np
import pandas as pd
import json
from sklearn.cross_validation import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn import tree
from sklearn.feature_extraction.text import CountVectorizer


data = json.load(open('linkStatusBuffer(1).json'))

vectorizer = CountVectorizer()

for i in data['title']:
	vectors = vectorizer.fit_transform(i)
	print vectors
# data preprocessing

# example structure of data: title, tags, description, maliciousLinksCount e.g [[title, tags, description, 5]]
# X_train = [[],[]]
# y_train = ['F','B','F','B','F']

# clf_entropy = DecisionTreeClassifier(criterion = "entropy", random_state = 100,
#  max_depth=3, min_samples_leaf=5)
# clf_entropy.fit(X_train, y_train)

# predictions = clf_entropy.predict(X_test)

# print "accuracy: " + str(accuracy_score(y_test,predictions)*100) + "%"



