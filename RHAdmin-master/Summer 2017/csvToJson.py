
import csv
import json

class csvToJson():

	def __init__(self, fileName):

		# generate new file name with appropriate extension
		csvFile = open(fileName + '.csv')
		jsonFile = fileName + '.json'

		# write to json file
		self.write(csvFile, jsonFile)
		

	def write(self, csvFile, jsonFile):

		csvReader = csv.reader(csvFile)
		next(csvReader, None) # Skip the first line
		jsonList = [] # creating a list for indexing and append
		group = set()


		# adding new entry to the jsonList
		for row in csvReader:
			newData = {'email':row[7], 'emailGroup': row[8][:3].lower()+'.summer.residents@rha.gatech.edu'}
			"""
				add to the summer residents list, with suffix: '.summer.residents@rha.gatech.edu'
			"""
			group.add(row[8][:3].lower()+'.summer.residents@rha.gatech.edu')
			jsonList.append(newData)

		# write the jsonList to json file
		with open(jsonFile, mode = 'w', encoding = 'utf-8') as j:
			json.dump(jsonList, j)

		csvGroupFile = open('group.csv', 'w', newline='')
		csvWriter = csv.writer(csvGroupFile)
		for aGroup in group:
			csvWriter.writerow([aGroup])


test = csvToJson('SummerList')

		 



