import configparser as parser

# Test reading config file
properties = parser.ConfigParser()
properties.read('./config.ini')

city = properties['CONFIG']['city']

print(city)

attendeeName = properties['CONFIG']['attendee']
print(attendeeName)

# Test csv file
import sys
import csv
with open('mileage.csv', 'r') as csvfile:
    f = csv.reader(csvfile, delimiter='\t', lineterminator="\r\n")
    lineno = 0;
    for values in f:
        lineno += 1
        comment = ""

        if (len(values) == 0) : continue

        if (len(values) == 1) : 
            if values[0].startswith("#") : continue

        if (len(values) < 5 or len(values) > 6) :
            print(f"Content of csv file is not proper. Line {lineno}: {values}" )
            print("Exmaple row is following" )
            print("05/02/2022	Home	HKMC	Short	100" )
            sys.exit()
        elif (len(values) == 6 ):
            trDate, fromLoc, toLoc, vehicleId, distance, comment = values
        elif (len(values) == 5 ):
            trDate, fromLoc, toLoc, vehicleId, distance = values

        distance = distance.strip()
        comment = comment.strip()

        print(trDate, fromLoc, toLoc, vehicleId, distance, comment)
        
