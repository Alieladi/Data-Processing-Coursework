import urllib.request
import sys
import time

time_interval = int(sys.argv[2])
total_time = int(sys.argv[3])
n = int(total_time / time_interval)
#print(str(n))
with open(sys.argv[1], "wb") as jsonFile: # wb: writing binary
	for i in range(n):
		data = urllib.request.urlopen("http://data.itsfactory.fi/journeys/api/1/vehicle-activity")
		jsonFile.write(data.read())
		time.sleep(time_interval)
		#print("hi")
