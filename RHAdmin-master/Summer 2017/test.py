from __future__ import print_function
import httplib2
import os
import json
import csv
import sys

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/admin-directory_v1-python-quickstart.json
SCOPES = ['https://www.googleapis.com/auth/admin.directory.group','https://www.googleapis.com/auth/admin.directory.user',
'https://www.googleapis.com/auth/admin.directory.domain','https://www.googleapis.com/auth/admin.directory.resource.calendar',
'https://www.googleapis.com/auth/admin.directory.customer', 'https://www.googleapis.com/auth/admin.directory.userschema'
]
CLIENT_SECRET_FILE = 'RHA-DIA-1718-Client.json'
APPLICATION_NAME = 'Client for rha-dia-1718'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'admin-directory_v1-python-rha-dia-1718.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def get_resident_json():
    with open('SummerList.json') as j:
        data = json.load(j)
    return data

def getGroupLists():
    # aList = []
    # aList.append('glc.summer.residents@rha.gatech.edu')
    # aList.append('gln.summer.residents@rha.gatech.edu')
    # aList.append('hrn.summer.residents@rha.gatech.edu')
    # aList.append('nae.summer.residents@rha.gatech.edu')
    # aList.append('naw.summer.residents@rha.gatech.edu')
    # aList.append('nsl.summer.residents@rha.gatech.edu')
    # aList.append('thb.summer.residents@rha.gatech.edu')
    # aList.append('thd.summer.residents@rha.gatech.edu')
    # aList.append('the.summer.residents@rha.gatech.edu')
    # aList.append('thf.summer.residents@rha.gatech.edu')
    # aList.append('thg.summer.residents@rha.gatech.edu')
    # aList.append('wds.summer.residents@rha.gatech.edu')
    aList = []
    csvGroup = open('group.csv', 'r')
    csvReader = csv.reader(csvGroup)
    for item in csvReader:
        aList.append(item)
    return aList

def deleteExistingGroups(service, groupList):
    failed = []
    for aGroup in groupList:
        try:
            service.groups().delete(groupKey=aGroup).execute()
        except:
            print('Failed to delete group ' + str(aGroup) + ' Error Message: ' , sys.exc_info()[1])
            failed.append(aGroup)
    return failed

def addNewGroups(service, groupList):
    failed = []
    for aGroup in groupList:
        try:
            service.groups().insert(body=aGroup).execute()
        except:
            print('Failed to insert group ' + str(aGroup) + ' Error Message: ' , sys.exc_info()[1])
            failed.append(aGroup)
    return failed

# For president and dia
def addToAllGroups(service, userList, groupList):
    failed = []
    for aUser in userList:
        modifiedUser = {'email':aUser['email'], 'role':'MEMBER'}
        for aGroup in groupList:
            try:
                service.members().insert(groupKey=aGroup, body=aUser).execute()
            except:
                print('Failed to add user ' + aUser['email'] + ' to group ' + str(aGroup) + ' Error Message: ' , sys.exc_info()[1])
                temp = {'email':aUser['email'], 'emailGroup':aGroup}
                failed.append(temp)  
    return failed

def addAllAccess(service, userList, groupList):
    failed = []
    for aUser in userList:
        modifiedUser = {'email':aUser['email'], 'role':'OWNER'}
        for aGroup in groupList:
            try:
                service.members().update(groupKey=aGroup, memberKey=aUser['email'], body=modifiedUser).execute()
            except:
                print('Failed to update user ' + aUser['email'] + ' to group' + str(aGroup) + ' Error Message: ' , sys.exc_info()[1])
                temp = {'email': aUser['email'], 'emailGroup':aGroup}
                failed.append(temp)
    return failed

def updateToGroup(service, userList, aRole):
    failed = []
    for aUser in userList:
        modifiedUser = {'email':aUser['email'], 'role':aRole}
        try:
            service.members().update(groupKey=aUser['emailGroup'], body=modifiedUser).execute()
        except:
            print('Failed to update user ' + aUser['email'] + ' as OWNER to group ' + aUser['emailGroup'] + ' Error Message: ' , sys.exc_info()[1])
            failed.append(aUser)
    return failed

def addToGroup(service, userList, aRole):
    failed = []
    for aUser in userList:
        modifiedUser = {'email':aUser['email'], 'role': aRole}
        try:
            service.members().insert(groupKey=aUser['emailGroup'], body=modifiedUser).execute()
        except:
            print('Failed to add user ' + aUser['email'] + ' to group ' + aUser['emailGroup'] + ' Error Message: ' , sys.exc_info()[1])
            failed.append(aUser)
        finally:
            count = count + 1
            print(str(count) + ' processed')
    return failed

def main():

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('admin', 'directory_v1', http=http)

    groupList = getGroupLists()
    userList = ['president@rha.gatech.edu', 'dia@rha.gatech.edu', 'advisor@rha.gatech.edu', 'it@rha.gatech.edu']
    residentsList = get_resident_json()
    ############### Deleting existing groups for future updates ##########
    print('****************** DELETING ALL TARGET GROUPS **************************')
    failedList = deleteExistingGroups(service, groupList)
    while(len(failedList) != 0):
        failedList = deleteExistingGroups(service, failedList)
    ############### Adding president and dia to every existing groups ############
    print('****************** ADDING TO ALL GROUPS (PRESIDENT, DIA, ADVISOR, IT) *************************')
    failedList = addToAllGroups(service, userList, groupList)
    while(len(failedList) != 0):
        failedList = addToGroup(service, failedList, 'MEMBER')

    ############### Updating president, dia, advisor, it to every existing groups as OWNER ################
    print('******************** SETTING OWNERS (PRESIDENT, DIA, ADVISOR, IT) ********************')
    failedList = addAllAccess(service, userList, groupList)
    while(len(failedList) != 0):
        failedList = addToGroup(service, failedList, 'OWNER')

    ############### Adding all residents' list to Google Group #################
    print('***************** ADDING ALL RESIDENTS TO GROUPS ******************')
    failedList = addToGroup(service, residentsList, 'MEMBER')
    while(len(failedList) != 0):
        failedList = addToGroup(service, failedList, 'MEMBER')

    ############### Adding residents to the corresponding groups ###############
    # residentsList = get_resident_json()
    # count = 0
    # for aResident in residentsList:
    # 	try:
    #         residentInfo = {'email': aResident['email'], 'role': 'MEMBER'}
    #         residentGroup = getGroupKey(aResident)
    #         service.members().insert(groupKey=residentGroup, body=residentInfo).execute()
    #         success = open('success.csv', 'a')
    #         csvWriter = csv.writer(success)
    #         csvWriter.writerow([aResident['building'], residentGroup, aResident['email']])
    #     except:
    #         print('Failed to add to Group', sys.exc_info())
    #         leftOver = open('leftOver.csv', 'a')
    #         csvWriter = csv.writer(leftOver)
    #         csvWriter.writerow([aResident['email'], aResident['building']])
    #     finally:
    #         count = count + 1
    #         print(str(count) + ' processed', end='\r')


if __name__ == '__main__':
    main()