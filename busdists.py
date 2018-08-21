from mrjob.job import MRJob
import re, os, sys
from math import radians, cos, sin, asin, sqrt
WORD_RE = re.compile(r"[\w']+")

# haversine
def haversine(p1, p2):  # p1, p2 coordinate points of form [latitude, longitude].
    # Convert decimal degrees to radians (also ensures values are floats).
	pr1 = [radians(float(p1[0])), radians(float(p1[1]))]
	pr2 = [radians(float(p2[0])), radians(float(p2[1]))]

	# Haversine formula
	dlat = pr2[0] - pr1[0]   # Difference of latitudes.
	dlon = pr2[1] - pr1[1]   # Difference of longitudes.
	a = sin(dlat/2)**2 + cos(pr1[0]) * cos(pr2[0]) * sin(dlon/2)**2
	c = 2 * asin(sqrt(a)) 
	r = 6371 # Radius of earth in kilometers.
	return c * r
#compute distance along many sorted points
def nhaversine(dictvalues): # dictvalues [(latitude, longitude), ( ... , ... ), ...] later equal to perveh[value[i]]
	dist = 0
	
	for i in range(1,len(dictvalues)):
		if len(dictvalues)>1:
			#print(dictvalues[i-1], dictvalues[i])
			dist += haversine(dictvalues[i-1], dictvalues[i])
			#print(dist)
	return dist

class MRWordFreqCount(MRJob):
	MRJob.SORT_VALUES = True
	def mapper(self, _, line):
		linetab = line.split(',')
		if linetab[0]!="time":
			key = os.getenv('mapreduce_map_input_file') # the key
			values = (linetab[9], linetab[0], float(linetab[5]), float(linetab[4])) # (vehicleRef, time, latitude, longitude)
		
			yield key, values

	def reducer(self, key, values):
		perveh = {} # per vehicle e.g {vehicle: [pairs of (latitude, longitude)]}	
		for value in values:
			#print(value)
			if value[0] in perveh:
				perveh[value[0]].append((value[2], value[3]))
			else:
				perveh[value[0]] = [(value[2], value[3])]
		dist = {}
		for value in perveh:
			#print(perveh[value])
			dist[value] = nhaversine(perveh[value])
		sumdist = sum(dist.values())
		yield key, sumdist



if __name__ == '__main__':
	MRWordFreqCount.run()