import sys
import numpy as np
result = {}
f = open(sys.argv[1], "r")
input_string = f.read()
f.close() # vient d'être ajoutée
input_list_string = input_string.split(" ")
input_list = [] # items in float
for input in input_list_string:
	input_list.append(float(input))
#print(input_list)

minimum = np.amin(input_list)
maximum = np.amax(input_list)
average = np.average(input_list)
median = np.median(input_list)
variance = np.var(input_list)

print("Minimum: %s"% (minimum))
print("Maximum: %s"% (maximum))
print("Average: %s"% (average))
print("Median: %s"% (median))
print("Variance: %s"% (variance))
f.close()