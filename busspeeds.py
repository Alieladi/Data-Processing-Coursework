import io
import json
import sys
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from math import radians, cos, sin, asin, sqrt
# LL_90 or TKL_647 or LL_93 -> cmd: python busspeeds.py LL_93
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
# let's begin
argvehicle = sys.argv[1] # vehicle reference
datapoints = {}  # datapoints {record times: [location coordinates(x, y), speed]}

with open("busdata.json", "r") as busdata:
	databuf = io.StringIO()  # Initialize an empty StringIO file.
	for line in busdata:       # Read the original busdata file one line at a time.
		databuf.write(line)    # Write the read line into the StringIO file.
		if line == '}\n':      # Did we reach the end of a top-level dictionary?
			databuf.seek(0)    # Set the StringIO to enable reading from its beginning.
			data = json.load(databuf)   # Read the single top-level JSON dictionary.
			databuf.close()             # Discard the current StringIO object.
			databuf = io.StringIO()  # Initialize a new empty StringIO object.
			# Now data can be used as a normal Python dictionary.
			# print(data.keys())  # One example: lists the keys of the data dictionary.
			for bus in data["body"]:
				if bus["monitoredVehicleJourney"]["vehicleRef"] == argvehicle:
					vehicle = bus["monitoredVehicleJourney"]["vehicleRef"]
					recordTime = bus["recordedAtTime"]
					speed = bus["monitoredVehicleJourney"]["speed"]
					location = bus["monitoredVehicleJourney"]["vehicleLocation"]
				
					if recordTime not in datapoints:
						datapoints[recordTime] = [location["latitude"], location["longitude"], speed]


datapointsKeys = sorted(datapoints) # sort datapoints keys by increasing time 
								# (it works fine since the format of the time in the file helps)
speeds = [] # speeds according to data
for recordTime in datapointsKeys:
	speeds.append(datapoints[recordTime][2]) # index 2 -> speed

speeds2 = [speeds[0]] # calculated speeds
previousTimeStr = datapointsKeys[0] # first time in string format
previousTime = datetime.strptime(previousTimeStr, '%Y-%m-%dT%H:%M:%S.%f+03:00')
#print(previousTime)
p1 = datapoints[previousTimeStr][:2] # [:2] for index 0, 1

for recordTimeStr in datapointsKeys[1:]:
	recordTime = datetime.strptime(recordTimeStr, '%Y-%m-%dT%H:%M:%S.%f+03:00')
	timedifference = recordTime - previousTime
	timeSeconds = timedifference.total_seconds()
	timeHours = float(timeSeconds)/3600
	#print(timeSeconds)
	
	previousTime = recordTime
	p2 = datapoints[recordTimeStr][:2] # [:1] for index 0, 1
	distance = haversine(p1, p2)
	p1 = p2
	speed = float(distance) / timeHours
	speeds2.append(speed)
	
# we could also use ordereddict: see https://docs.python.org/3/library/collections.html#collections.OrderedDict
	
	
#print(speeds2)


plt.plot(speeds)
plt.plot(speeds2)
plt.savefig('busspeeds.png')   # This saves the graph into a file "busspeeds.png" 
plt.show()                     # This shows the graph in a windows
