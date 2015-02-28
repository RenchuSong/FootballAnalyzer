import csv
import matplotlib.pyplot as plt
import json

combine = []

def norm_name(name):

	i = len(name) - 1
	while i > -1 and not('a' <= name[i] <= 'z' or 'A' <= name[i] <= 'Z'):
		i -= 1
	return name[0:i+1]

with open('combine.csv', 'rb') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',')
	i = 0
	
	for row in spamreader:
		i += 1
		if i > 1:
			if int(row[0]) <= 2011 and row[4] == 'WR':
				combine.append({
					'name' : row[1],
					'year' : row[0],
					'fortyyd' : row[10],
					'twentyss' : row[13],
					'vertical' : row[15],
					'bench' : row[17]
				})

receivingdata = []
for y in range(2000, 2015):
	with open(str(y) + 'ReceivingYards.csv', 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',')
		i = 0

		item = []
		
		for row in spamreader:
			i += 1
			if i > 2:
				item.append(row)
		
		receivingdata.append(item)

data = []

pair = {
	'G' : 4,
	'GS' : 5,
	'Tgt' : 6,
	'Rec' : 7,
	'Yds' : 8,
	'Y/R' : 9,
	'TD' : 10,
	'Lng' : 11,
	'R/G' : 12,
	'Y/G' : 13,
	'Fmb' : 14
}

for person in combine:
	year = int(person['year']) - 1999
	for year_after in range(0, 3):
		year_data = receivingdata[year + year_after]
		for d in year_data:
			if person['name'] == norm_name(d[1]):
				for key in pair:
					if len(d[pair[key]]) > 0:
						if not key in person:
							person[key] = float(d[pair[key]])
						else:
							person[key] += float(d[pair[key]])

	for key in pair:
		if key in person:
			person[key] /= 3.0
		else:
			person[key] = 0

	data.append(person)

print json.dumps(data)				
				
				




