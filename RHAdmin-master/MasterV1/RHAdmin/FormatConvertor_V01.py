# This class is used for converting a standard resident list to the desired JSON format

import csv
import json
import re

class FormatConvertor:

	def convert_byArea(self, fileName, term): # term = 0--summer; term = 1--not summer
		csvFile = open(fileName)
		csvReader = csv.reader(csvFile)
		info = False
		jsonList = []

		area_index = 0
		lastName_index = 0
		firstName_index = 0
		gtid_index = 0
		room_index = 0
		email_index = 0

		areaList = []
		resHallList = []

		for row in csvReader:
			if(info):
				studentInfo = {'FirstName': row[firstName_index], 'LastName': row[lastName_index], 'Email': row[email_index], 'GTID': row[gtid_index]}

				firstName = row[firstName_index]
				lastName = row[lastName_index]
				email = row[email_index]
				gtid = row[gtid_index]
				if (term == 0):
					resHallGroup = row[room_index][:3].lower() + '.summer.residents@rha.gatech.edu'
				elif(term == 1):
					resHallGroup = row[room_index][:3].lower() + '.residents@rha.gatech.edu'
				area = re.sub('\s', '', row[area_index].lower())

				#print(firstName, lastName, email, gtid, resHallGroup, area)


				studentInfo = [{'FirstName': row[firstName_index], 'LastName': row[lastName_index], 'Email': row[email_index], 'GTID': row[gtid_index]}]
				if (resHallGroup in resHallList):
					jsonList[areaList.index(area)][resHallList.index(resHallGroup)].append(studentInfo)

				elif(area in areaList):
					resHallList.append(resHallGroup)
					temp = {'ResHallGroup': resHallGroup, 'StudentInfo': [studentInfo]}
					jsonList[areaList.index(area)].append(temp)
				else:
					areaList.append(area)
					resHallList.append(resHallGroup)
					temp = [{'ResHallGroup': resHallGroup, 'StudentInfo': [studentInfo]}]
					temp = {'Area': area, 'Detail': [temp]}
			else:
				area_index = row.index("area")
				lastName_index = row.index("lastName")
				firstName_index = row.index("firstName")
				gtid_index = row.index("gtid")
				room_index = row.index("room")
				email_index = row.index("email")
				info = True

		return jsonList

	#def convert_byGTID(self, fileName):

