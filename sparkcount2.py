from pyspark import SparkContext
def main():
	sc = SparkContext(appName='SparkWordCount')
	input_file = sc.textFile('/user/student/americana/')
	stopwords = set()
	with open("stopwords.txt", "r") as swfile:
			for stopword in swfile.read().split(","):
				stopwords.add(stopword)
	br_stopwords = sc.broadcast(stopwords)
	counts = input_file.flatMap(lambda line: line.split()) \
	.filter(lambda word: word not in br_stopwords.value)\
	.map(lambda word: (word, 1)) \
	.reduceByKey(lambda a, b: a + b)
	counts.saveAsTextFile('/user/student/test18/4_3')
	sc.stop()
if __name__ == '__main__':
	main()
# spark-submit sparkcount2.py
# then check:
# hdfs dfs -ls /user/student/test18/4_3
# hdfs dfs -tail /user/student/test18/4_3/part-00000