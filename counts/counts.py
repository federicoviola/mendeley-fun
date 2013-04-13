import json
import datetime

data = json.load( open('../all.json', 'r') )

dates = {}

for d in data:
	date = str( datetime.date.fromtimestamp( d['added'] ) )
	if date not in dates:
		dates[ date ] = 0
	dates[ date ] = dates[ date ] + 1

for d in sorted( dates ):
	print d + ':' + str( dates[ d ] )
