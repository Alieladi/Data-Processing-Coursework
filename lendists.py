from mrjob.job import MRJob
import re, os, json, io, collections
from mrjob import protocol
from mrjob.step import MRStep

WORD_RE = re.compile(r"[\w']+")


class MRWordFreqCount(MRJob):
	OUTPUT_PROTOCOL = protocol.JSONValueProtocol
	# it's by default: INTERNAL_PROTOCOL = protocol.SimpleJSONProtocol
	MRJob.SORT_VALUES = True
	def mapper(self, _, line):
		for word in WORD_RE.findall(line):
			file_name = os.getenv('mapreduce_map_input_file')
			f_len = (file_name, len(word))
			yield f_len, 1

	def reducer1(self, f_len, occurrences):
		file_name = f_len[0]
		wlength = str(f_len[1])
		count = sum(occurrences)
		len_count = (wlength, count)
		yield file_name, len_count
	def reducer2(self, file_name, len_counts):
		jsonRes = dict(len_counts)
		jsonRes['file'] = file_name
		yield None, collections.OrderedDict(sorted(jsonRes.items(), key=lambda t: t[0]))
	def steps(self):
		return [
			MRStep(mapper=self.mapper,
				reducer=self.reducer1),
			MRStep(reducer=self.reducer2)
		]
if __name__ == '__main__':
	MRWordFreqCount.run()