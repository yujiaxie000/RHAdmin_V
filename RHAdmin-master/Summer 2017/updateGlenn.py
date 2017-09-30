
import csv
import json

class updateGlenn():

	def __init__(self, fileName, resHallName=None, specification=None):

		# generate new file name with appropriate extension
		csvFile = open(fileName + '.csv')
		jsonFile = fileName + '.json'

		# write to json file
		self.write(csvFile, jsonFile, resHallName, specification)
		

	def write(self, csvFile, jsonFile, resHallName=None, specification=None):

		csvReader = csv.reader(csvFile)
		next(csvReader, None) # Skip the first line
		jsonList = [] # creating a list for indexing and append
		group = set()


		# adding new entry to the jsonList
		for row in csvReader:
			if resHallName != None and specification != None:
				if row[9][:3] == resHallName and specification in row[11]:
					#print(row[11], row[9][:3])
					newData = {'email':row[8], 'emailGroup': row[9][:3].lower()+'.summer.residents@rha.gatech.edu'}
					"""
						add to the summer residents list, with suffix: '.summer.residents@rha.gatech.edu'
					"""
					group.add(row[9][:3].lower()+'.summer.residents@rha.gatech.edu')
					jsonList.append(newData)
			else:
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


test = updateGlenn('SummerListUpdated', 'GLN', 'Late')

		 



