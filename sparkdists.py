from pyspark import SparkContext
import json
def main():
	sc = SparkContext(appName='SparkWordCount')
	input_files = sc.wholeTextFiles('/user/student/americana/') # pairs (filename, file contents)
	lengths = input_files.flatMap(lambda input_pair: [(input_pair[0],len(word))for word in input_pair[1].split()])

	counts = lengths.map(lambda length: (length, 1))\
			.reduceByKey(lambda a, b: a + b)
	res = counts.collect()
	res_dict = {}
	for tuple in res:
		if tuple[0][0] in res_dict:
			res_dict[tuple[0][0]] += ", "+str(tuple[0][1])+" : "+str(tuple[1])
		else:
			res_dict[tuple[0][0]] = "{\"file\" : \" "+str(tuple[0][0])+"\", "+str(tuple[0][1])+" : "+str(tuple[1])
	for file_names in res_dict:
		res_dict[file_names] += "} \n"
	with open("lendists.json", "a") as lendists:
		for res_per_file in res_dict.values():
			lendists.write(res_per_file)
	#json.dump(res, "lendists.json")
	sc.stop()
if __name__ == '__main__':
	main()

# spark-submit sparkdists.py

