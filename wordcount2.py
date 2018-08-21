from mrjob.job import MRJob
from mrjob.step import MRStep
import re

WORD_RE = re.compile(r"[\w']+")




class MRWordFreqCount(MRJob):
	def mapper_init(self):
		with open("stopwords.txt", "r") as swfile:
			self.stopwords = swfile.read().split(",")
	def mapper(self, _, line):
		"""with open("stopwords.txt", "r") as swfile:
			stopwords = swfile.read().split(",")"""
		for word in WORD_RE.findall(line):
			if word not in self.stopwords:
				yield word.lower(), 1

	def combiner(self, word, counts):
		yield word, sum(counts)

	def reducer(self, word, counts):
		yield word, sum(counts)


if __name__ == '__main__':
	MRWordFreqCount.run()



