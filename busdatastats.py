import io
import json

busLines = set() # set of bus lines numbers
vehicles = {}    # vehicles {bus line number: set of vehicles references}
datapoints = {}  # datapoints {bus line number:{vehicle: set of record times}}

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
			for bus in data["body"]:
				busLine = bus["monitoredVehicleJourney"]["lineRef"]
				vehicle = bus["monitoredVehicleJourney"]["vehicleRef"]
				recordTime = bus["recordedAtTime"]
				# add busLine to the set of busLines
				busLines.add(busLine)
				# add vehicle to the set of vehicles of the busLine
				# Plus, add recordTime to the set of recordTimes of the vehicle in the busLine
				if busLine in vehicles:
					vehicles[busLine].add(vehicle)
					if vehicle in datapoints[busLine]: # add recordTime
						datapoints[busLine][vehicle].add(recordTime)
					else:
						datapoints[busLine][vehicle] = {recordTime}
				else:
					vehicles[busLine] = {vehicle}
					datapoints[busLine] = {vehicle: {recordTime}}

busLinesKeys = sorted(busLines)
for busLineKey in busLinesKeys:
	a1 = busLineKey
	a2 = len(vehicles[busLineKey])
	a3 = 0
	# counting datapoint
	for vehicle in datapoints[busLineKey].values(): ## or sum
		a3 += len(vehicle)
	print("%s : %d vehicules and %d data points" % (a1, a2, a3))
	
