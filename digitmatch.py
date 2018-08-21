from PIL import Image
from PIL import ImageFilter
import numpy as np
from sklearn import datasets, svm, metrics

img = Image.open("9.png")
pixels = img.load() # create the pixel map
XY = []

for i in range(img.size[0]):    # for every pixel: size[0] -> x
	for j in range(img.size[1]):	# size[1] -> y
		r = pixels[i,j][0]
		g = pixels[i,j][1]
		b = pixels[i,j][2]
		if (r + 15 <= b) and (g + 15 <= b):
			pixels[i,j] = (0, 0, 0)
			XY.append([i,j])
		else:
			pixels[i,j] = (255, 255, 255)

XYmaxX = max(XY, key = lambda x: x[0])
XYminX = min(XY, key = lambda x: x[0])
XYmaxY = max(XY, key = lambda x: x[1])
XYminY = min(XY, key = lambda x: x[1])

croppedImg = img.crop((XYminX[0], XYminY[1], XYmaxX[0], XYmaxY[1])) # 4-tuple defining the left, upper, right, and lower pixel coordinate.
squareSide = max(XYmaxX[0] - XYminX[0], XYmaxY[1] - XYminY[1])
squareImg = Image.new("RGB", (squareSide, squareSide), "white")
marginX = int((squareSide - XYmaxX[0] + XYminX[0])/2)
marginY = int((squareSide - XYmaxY[1] + XYminY[1])/2)
squareImg.paste(croppedImg, (marginX, marginY))

resizedImg = squareImg.resize((16, 16))
convertedImg = resizedImg.convert("L")
filteredImg = convertedImg.filter(ImageFilter.Kernel((3,3), [0.0625, 0.125, 0.0625, 0.125, 0.25, 0.125, 0.0625, 0.125, 0.0625]))

bipixels = [] # 8x8 two-dimensional list
mydata = [] # for 64 size one-dimensional list
filteredPixels = filteredImg.load() # create the pixel map

for j in range(8):
	bipixels.append([])
	for i in range(8):
		JI = np.average([filteredPixels[2*i,2*j], filteredPixels[2*i+1, 2*j], filteredPixels[2*i, 2*j+1], filteredPixels[2*i+1, 2*j+1]])
		bipixels[j].append(JI)
		bipixels[j][i] = (256 - bipixels[j][i])/16
		mydata.append(bipixels[j][i])
"""		
for j in range(8):
	for i in range(8):
		bipixels[j][i] =  (256 - bipixels[i, j])/16.
"""
#filteredImg.show()

classifier = svm.SVC(gamma=0.001) 
digits = datasets.load_digits()
n_samples = len(digits.images)
traindata = digits.images.reshape(n_samples, -1) # http://docs.scipy.org/doc/numpy/reference/generated/numpy.reshape.html
# training the classifier
classifier.fit(traindata[:], digits.target[:n_samples])
print("prediction for the image that you chose is: ")
print(classifier.predict(mydata))
# result for	0 1 2 3 4 5 6 7 8 9
#	is:			1 1 2 3 4 5 6 9 8 9

