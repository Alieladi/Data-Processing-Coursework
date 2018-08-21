from pyspark import SparkContext
import re
def preprocess(line):
	def split_line():
		splitted_line = line.split(",")
		hour = splitted_line[0][11:13]
		linRef = splitted_line[1]
		speed = splitted_line[14]
		return (hour, (hour,lineRef,speed))
	return split_line
	
def plotting_func(data):
	datapts = data[1]
	import matplotlib as mpl
	mpl.use('Agg')
	import matplotlib.pyplot as plt
	dataset = {}
	for datapt in datapts:
		if datapt[1] in dataset:
			dataset[datapt[1]].append(datapt[2])
		else:
			dataset[datapt[1]] = datapt[2]
	dt_labels = []
	dt = []
	for data in dataset:
		dt_labels.append(data)
		dt.append(dataset[data])
		
	plt.boxplot(dt, labels=dt_labels)
	plot_name = "speedbox_"+datapts[2]
	plt.savefig(plot_name)
	
	import pydoop.hdfs as phdfs
	import pydoop.hdfs.path as hpath
	local_path = hpath.abspath(plot_name, local=True)
	phdfs.put(local_path, "/user/student/test18/")
	#plt.show()
	import os
	os.environ['JAVA_HOME'] = '/usr/java/latest'
	import pydoop.hdfs as hdfs
	os.remove(local_path)
	"""Create a plot,
		save it to a local file,
		copy the file to HDFS,
		and delete the local file. """
def main():
	sc = SparkContext(appName='SparkWordCount')
	input_file = sc.textFile('/user/student/busdata/j*')

	speedplot = input_file.filter(lambda line: 'time' != line[:4] )\
	.map(preprocess)\
	.reduceByKey(plotting_func)
	sc.stop()
if __name__ == '__main__':
	main()
# spark-submit hourspeedboxes.py
# then check:
# hdfs dfs -ls /user/student/test18/4_3
# hdfs dfs -tail /user/student/test18/4_3/part-00000
