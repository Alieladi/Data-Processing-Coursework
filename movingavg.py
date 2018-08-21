from mrjob.job import MRJob
import re, os, sys, numpy

WORD_RE = re.compile(r"[\w']+")



class MRWordFreqCount(MRJob):
	m = 2
	def mapper(self, _, line):
		pair = line.split(' ')
		for i in range(self.m):
			yield int(pair[0])+i, pair[1]

	def reducer(self, key, values):
		somme = 0
		for value in values:
			somme += float(value)
		mavg = somme/self.m
		yield key, mavg



if __name__ == '__main__':
	MRWordFreqCount.run()