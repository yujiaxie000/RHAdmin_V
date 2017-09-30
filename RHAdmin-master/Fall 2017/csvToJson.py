
import csv
import json
import re

class csvToJson(): # Version 2

	def __init__(self, fileName):

		# generate new file name with appropriate extension
		csvFile = open(fileName + '.csv')
		jsonFile = fileName + '.json'
		updateJsonFile = fileName + 'Updated.json'

		# write to json file
		self.write(csvFile, jsonFile)
		

	def write(self, csvFile, jsonFile):

		csvReader = csv.reader(csvFile)
		next(csvReader, None) # Skip the first line
		jsonList = [] # creating a list for indexing and append
		group = set()
		area = set() # fall/spring list is too large to run at one time


		# adding new entry to the jsonList
		for row in csvReader:
			newData = {'email':row[5], 'emailGroup': row[4][:3].lower()+'.residents@rha.gatech.edu', 'area': re.sub('\s','', row[7].lower())}
			"""
				add to the summer residents list, with suffix: '.summer.residents@rha.gatech.edu'
			"""
			group.add(row[4][:3].lower()+'.residents@rha.gatech.edu')
			area.add(re.sub('\s','', row[7].lower()))
			jsonList.append(newData)

		# write the jsonList to json file
		with open(jsonFile, mode = 'w', encoding = 'utf-8') as j:
			json.dump(jsonList, j)

		csvGroupFile = open('group.csv', 'w', newline='')
		csvWriter = csv.writer(csvGroupFile)
		for aGroup in group:
			csvWriter.writerow([aGroup])

		csvAreaFile = open('area.csv', 'w', newline='')
		csvWriter2 = csv.writer(csvAreaFile)
		for aArea in area:
			csvWriter2.writerow([aArea])

	def update(self, csvFile, jsonFile, resHallName, specification):
		csvReader = csv.reader(csvFile)
		next(csvReader, None)
		jsonList = []
		group = set()

		for row in csvReader:
			if resHallName == row[4][:3] and specification in row[-1]:
				newData = {'email':row[5], 'emailGroup': row[4][:3].lower()+'.residents@rha.gatech.edu'}
				"""
					add to the summer residents list, with suffix: '.summer.residents@rha.gatech.edu'
				"""
				group.add(row[4][:3].lower()+'.residents@rha.gatech.edu')
				jsonList.append(newData)		

		# write the jsonList to json file
		with open(jsonFile, mode = 'w', encoding = 'utf-8') as j:
			json.dump(jsonList, j)

		csvGroupFile = open('groupUpdated.csv', 'w', newline='')
		csvWriter = csv.writer(csvGroupFile)
		for aGroup in group:
			csvWriter.writerow([aGroup])		


"""
00: Last Name
01: First Name
02: GTID
03: Gender
04: Room
05: Email
06: Term Code
07: Area
"""
test = csvToJson('FallListV0')

		 



