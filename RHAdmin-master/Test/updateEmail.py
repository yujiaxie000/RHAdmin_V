import csv

def csvToList(fileName):
    aList = []
    with open(fileName + ".csv", "r") as f:
        csvReader = csv.reader(f)
        next(csvReader, None)
        for row in csvReader:
            newData = {'name':{'familyName':row[0],'givenName':row[1]},'userKey':row[2],'primaryEmail':row[2],'password':row[3],'oldEmail':row[10], 'positionUpdate':row[9]}
            aList.append(newData)
    return aList



if __name__ == '__main__':
    print(csvToList('Email'))

