import json

data = json.load(open('linkStatusBuffer(1).json'))
scores = json.load(open('sampleClassifier.json'))

truePos = 0
falsePos = 0
trueNeg = 0
falseNeg = 0
unClass = 0
false = []
for i in range(len(data['videoId'])):
	threshold = 20
	if len(data['description'][i]) == 0:
		threshold -= 10
	if data['tags'][i] == 'No tags':
		threshold -= 5
	if scores[data['videoId'][i]] > threshold and data['classification'][i] == 'f':
		truePos += 1
	elif scores[data['videoId'][i]] > threshold and data['classification'][i] == 'b':
		falsePos += 1
		false.append([scores[data['videoId'][i]],data['videoId'][i]])
	elif scores[data['videoId'][i]] <= threshold and data['classification'][i] == 'f':
		falseNeg += 1
	elif scores[data['videoId'][i]] <= threshold and data['classification'][i] == 'b':
		trueNeg += 1
	else:
		unClass += 1

print 'TruePositive:',truePos
print 'FalsePositive',falsePos
print 'FalseNegative',falseNeg
print 'TrueNegative',trueNeg
print false
print 'unClass:',unClass