import configparser as parser

properties = parser.ConfigParser()
properties.read('./config.ini')

city = properties['CONFIG']['city']

print(city)

attendeeName = properties['CONFIG']['attendee']

print(attendeeName)
