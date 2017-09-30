import json
import csv

with open('SummerList.json') as j:
	data = json.load(j)

for element in data:
	leftOver = open('leftOver.csv', 'a')
	csvWriter = csv.writer(leftOver)
	csvWriter.writerow([element['role'], element['email'], element['building']])