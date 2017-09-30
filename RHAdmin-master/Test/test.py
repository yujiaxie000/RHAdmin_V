import csv

testFile = open('roster.csv')

csvReader = csv.reader(testFile)
next(csvReader, None)

aDict = {}

for row in csvReader:
    if row[4] in aDict.keys():
        aDict[row[4]] = aDict[row[4]] + 1
    else:
        aDict[row[4]] = 1
# print(aDict)

overDict = {'BSH':0, 'CREEE':0, 'CSA':0, 'ESSW': 0, 'FCF':0, 'FFM': 0, 'GLC': 0, 'Glenn': 0,'HA':0, 'HHC':0, 'GFSH':0, 'IMP':0, 'NAE':0, 'NANW':0, 'NAS':0, 'NSL':0, 'TH':0, 'WDF':0, 'ZBM':0}



for hc, num in aDict.items():
    if hc == 'GLN':
        overDict['Glenn'] += num
    elif hc == 'NAE':
        overDict['NAE'] += num
    elif hc == 'SMT' or hc == 'BRN' or hc == 'HRS':
        overDict['BSH'] += num
    elif hc == 'GLD' or hc == 'FLD' or hc == 'HOP' or hc == 'STN':
        overDict['GFSH'] += num
    elif hc == 'TOW' or hc == 'HAN':
        overDict['TH'] += num
    elif hc == 'PER' or hc == 'GRY' or hc == 'HAY' or hc == 'MTH':
        overDict['IMP'] += num
    elif hc == 'NAS':
        overDict['NAS'] += num
    elif hc == 'FLK' or hc == 'CAL' or hc == 'FUL':
        overDict['FCF'] += num
    elif hc == 'CSN' or hc == 'CSS':
        overDict['CSA'] += num
    elif hc == 'FRE' or hc == 'FIT' or hc == 'MON':
        overDict['FFM'] += num
    elif hc == 'NAW' or hc == 'NAN':
        overDict['NANW'] += num
    elif hc == 'MLD' or hc == 'ZBR':
        overDict['ZBM'] += num
    elif hc == 'CRE' or hc == 'ESE':
        overDict['CREEE'] += num
    elif hc == 'ESS' or hc == 'ESW':
        overDict['ESSW'] += num
    elif hc == 'GLC' or hc == 'THA' or hc == 'THB' or hc == 'THD' or hc == 'THC' or hc == 'THE' or hc == 'THF' or hc == 'THG':
        overDict['GLC'] += num
    elif hc == 'ARM' or hc == 'HEF':
        overDict['HA'] += num
    elif hc == 'CLD' or hc == 'HOW' or hc == 'HRN':
        overDict['HHC'] += num
    elif  hc == 'NSL':
        overDict['NSL'] += num
    elif hc == 'WDN' or hc == 'WDS':
        overDict['WDF'] += num
    else:
        print(hc, num)

for hc, num in overDict.items():
    print(hc, num)



