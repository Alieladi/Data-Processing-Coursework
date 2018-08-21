import io
import json

with open("busdata.json", "r") as busdata:
	databuf = io.StringIO()  # Initialize an empty StringIO file.
	for line in busdata: # Read the original busdata file one line at a time.
		print(line)
		databuf.write(line)    # Write the read line into the StringIO file.
		if line == '}\n':      # Did we reach the end of a top-level dictionary?
			print("hiaiaia")
			databuf.seek(0)    # Set the StringIO to enable reading from its beginning.
			data = json.load(databuf)   # Read the single top-level JSON dictionary.
			databuf.close()             # Discard the current StringIO object.
			databuf = io.StringIO()  # Initialize a new empty StringIO object.
			# Now data can be used as a normal Python dictionary.
			with open("outfile2.json", "a") as busfile:
				json.dump(data, busfile)
				busfile.write("\n")
			
			
	
