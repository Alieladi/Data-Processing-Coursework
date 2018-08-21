import sys
result = {}
input_list = []
for n in sys.argv[1:]: # or range(1,len(sys.argv)
	input_list.append(sys.argv[n]) # also outside for input_list = sys.argv[1:len(sys.argv)]
	for i in range(len(input_list[n-1])-1): 
		k = input_list[n-1][i]+input_list[n-1][i+1] #-------------- or input_list[n-1][i:i+2]
		if k not in result:
			result[k] = 1
		else:
			result[k] += 1

sorted_ab = sorted(result)
for ab in sorted_ab:
	print("%s: %s occurences"%(ab, result[ab]))
#print(sys.argv[0])