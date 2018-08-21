import sys
result = {}
input_list = []
for n in sys.argv[1:]: # or range(1,len(sys.argv)
	input_list.append(n) # also outside for input_list = sys.argv[1:len(sys.argv)]
	for i in range(len(n)-1):
		k = n[i]+ n[i+1]
		if k not in result:
			result[k] = 1
		else:
			result[k] += 1

sorted_ab = sorted(result)
for ab in sorted_ab:
	print("%s: %s occurences"%(ab, result[ab]))
#print(sys.argv[0])