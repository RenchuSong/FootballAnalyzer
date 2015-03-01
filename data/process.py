import csv
import matplotlib.pyplot as plt
import json

combine = []

def norm_name(name):
	i = len(name) - 1
	while i > -1 and not('a' <= name[i] <= 'z' or 'A' <= name[i] <= 'Z'):
		i -= 1
	return name[0:i+1]

def percentile(d, min, max):
	return float(d - min) / (max - min)

with open('combine.csv', 'rb') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',')
	i = 0
	
	for row in spamreader:
		i += 1
		if i > 1:
			if 2000 <= int(row[0]) <= 2012 and row[4] == 'WR':
				combine.append({
					'year' : row[0],
					'name' : row[1],
					'fortyyd' : float(row[10]),
					'twentyss' : float(row[13]),
					'vertical' : float(row[15]),
					'bench' : float(row[17]),
					'playyear' : 0,
					'picktotal' : int(row[22]),
					'weight' : float(row[7]),
					'arms' : float(row[8]),
					'hands' : float(row[9]),
					'tenyd' : float(row[12]),
					'threecone' : float(row[14]),
					'broad' : float(row[16]),
					'height' : float(row[23]),
				})

receivingdata = []
for y in range(2000, 2015):
	with open(str(y) + 'ReceivingYards.csv', 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',')
		item = []
		
		for row in spamreader:
			try:
				int(row[0])
				item.append(row)
			except Exception:
				pass
		
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
	year = int(person['year']) - 2000
	for year_after in range(0, 3):
		year_data = receivingdata[year + year_after]
		for d in year_data:
			if person['name'] == norm_name(d[1]):
				person['playyear'] += 1
				for key in pair:
					if len(d[pair[key]]) > 0:
						if not key in person:
							person[key] = float(d[pair[key]])
						else:
							person[key] += float(d[pair[key]])

	for key in pair:
		if key in person:
			person[key] /= person['playyear']
		else:
			person[key] = 0

	data.append(person)

max_fortyyd = min([float(p['fortyyd']) for p in data if p['fortyyd'] > 0 and p['twentyss'] > 0 and p['vertical'] > 0])
min_fortyyd = max([float(p['fortyyd']) for p in data if p['fortyyd'] > 0 and p['twentyss'] > 0 and p['vertical'] > 0])
max_twentyss = min([float(p['twentyss']) for p in data if p['fortyyd'] > 0 and p['twentyss'] > 0 and p['vertical'] > 0])
min_twentyss = max([float(p['twentyss']) for p in data if p['fortyyd'] > 0 and p['twentyss'] > 0 and p['vertical'] > 0])
max_vertical = min([float(p['vertical']) for p in data if p['fortyyd'] > 0 and p['twentyss'] > 0 and p['vertical'] > 0])
min_vertical = max([float(p['vertical']) for p in data if p['fortyyd'] > 0 and p['twentyss'] > 0 and p['vertical'] > 0])


max_yg = max([float(p['Y/G']) for p in data if p['Y/G'] > 0 and p['R/G'] > 0 and p['G'] > 0])
min_yg = min([float(p['Y/G']) for p in data if p['Y/G'] > 0 and p['R/G'] > 0 and p['G'] > 0])
max_rg = max([float(p['R/G']) for p in data if p['Y/G'] > 0 and p['R/G'] > 0 and p['G'] > 0])
min_rg = min([float(p['R/G']) for p in data if p['Y/G'] > 0 and p['R/G'] > 0 and p['G'] > 0])
max_g = max([float(p['G']) for p in data if p['Y/G'] > 0 and p['R/G'] > 0 and p['G'] > 0])
min_g = min([float(p['G']) for p in data if p['Y/G'] > 0 and p['R/G'] > 0 and p['G'] > 0])


filtered_data = []

for person in data:
	# if person['fortyyd'] > 0 and person['twentyss'] > 0 and person['vertical'] > 0 and person['name'] != 'Steve Smith':
	if person['name'] != 'Steve Smith':
		person['avgpercentile'] = (
			percentile(person['fortyyd'], min_fortyyd, max_fortyyd) +
			percentile(person['twentyss'], min_twentyss, max_twentyss) +
			percentile(person['vertical'], min_vertical, max_vertical)
		) / 3.0
		person['combinemetric'] = (
			percentile(person['Y/G'], min_yg, max_yg) +
			percentile(person['R/G'], min_rg, max_rg)
			# percentile(person['G'], min_g, max_g)
		) / 2.0
		filtered_data.append(person)

# print max_fortyyd, min_fortyyd
# print max_twentyss, min_twentyss
# print max_vertical, min_vertical

print json.dumps(filtered_data)		





