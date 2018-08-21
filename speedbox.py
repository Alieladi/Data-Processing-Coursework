import io
import json
import sys
import numpy
# let's begin

recordTimes = {} # record times {busLine: list of record times}
speeds = {} # speeds {busLine: list of speeds} for less complication
vehicles = []
avgspeeds = {} # average speed {busLine: average speed}
# average speed = sum(speed x timespan)/ total(timespan)
# but it's too complicated so I'll just do average speed = avg(speeds)

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
				vehicle = bus["monitoredVehicleJourney"]["vehicleRef"]
				busLine = bus["monitoredVehicleJourney"]["lineRef"]
				recordTime = bus["recordedAtTime"]
				speed = bus["monitoredVehicleJourney"]["speed"]
				if vehicle in recordTimes:
					if recordTime not in recordTimes[vehicle]:
						recordTimes[vehicle][recordTime] = speed
						speeds[busLine].append(float(speed))
				else:
					recordTimes[vehicle] = {recordTime: speed}
					#vehicles.append(vehicle)
					speeds[vehicle] = [float(speed)]

with open("avgs.txt", "w") as of:
	for busLine in speeds:
		avgspeeds[busLine] = numpy.mean(speeds[busLine])# here it's supposed to be mean(speads)
		of.write(str(avgspeeds[busLine]) + " ")
	of.write("\n")
print(avgspeeds.values())
