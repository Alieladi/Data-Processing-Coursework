from sklearn.linear_model import Perceptron
import numpy as np

# Perceptron
# train
trainItems = np.loadtxt("vertigo_train.txt") # loads all lines with same length (if 2 consecutive lines do not it stops reading)
data = []
classes = []
for item in trainItems:
	data.append(item[1:])
	classes.append(item[0])
p = Perceptron()
p.fit(data, classes)

# predict
test = np.loadtxt("vertigo_predict.txt")
ppredictions = p.predict(test)

#compare with answers
answers = np.loadtxt("vertigo_answers.txt")
testLength = len(test)
currentCorrect1 = 0
for i in range(testLength): # also matches(A, B)
	if(answers[i] == ppredictions[i]):
		currentCorrect1 += 1
percentageCorrect1 = float(currentCorrect1)/testLength
print("perceptron: " + str(percentageCorrect1))

# Nearest neighbor
nnpredictions = []
currentCorrect2 = 0
p = 0 # key of X
for X in test:
	dist = [] # list of distances between X and neighbors
	for Y in data:
		dist.append(sum([abs(x_i - y_i) for x_i, y_i in zip(X, Y)])) # check zip function
	nearestNeighbor = np.argmin(dist)
	nnprediction = classes[nearestNeighbor]
	nnpredictions.append(nnprediction) # store predictions in a list
	if(answers[p] == nnprediction):
		currentCorrect2 += 1
	p += 1
percentageCorrect2 = float(currentCorrect2)/testLength
print("Nearest neighbor: " + str(percentageCorrect2))
# also print(accuracy_score(answers, test results)