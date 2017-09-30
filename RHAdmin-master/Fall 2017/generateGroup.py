import httplib2
import os
import json
import csv
import sys
import logging

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

class RHAdmin():

    def __init__(self, client_secret, application_name):
        try:
            import argparse
            self.flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
        except ImportError:
            self.flags = None

        self.SCOPES = ['https://www.googleapis.com/auth/admin.directory.group',
                        'https://www.googleapis.com/auth/admin.directory.user',
                        'https://www.googleapis.com/auth/admin.directory.domain',
                        'https://www.googleapis.com/auth/admin.directory.resource.calendar',
                        'https://www.googleapis.com/auth/admin.directory.customer',
                        'https://www.googleapis.com/auth/admin.directory.userschema']

        self.CLIENT_SECRET_FILE = 'RHA-DIA-1718-Client.json'
        self.APPLICATION_NAME = 'Client for rha-dia-1718'

    def get_credentials(self):
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
            flow = client.flow_from_clientsecrets(self.CLIENT_SECRET_FILE, self.SCOPES)
            flow.user_agent = self.APPLICATION_NAME
            if self.flags:
                credentials = tools.run_flow(flow, store, self.flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials

    def authenticate(self):
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('admin', 'directory_v1', http=http)
        return service

    def get_resident_json(self,fileName): # residents list, json file
        with open (fileName + '.json') as j:
            data = json.load(j)
        return data

    def getList(self,fileName): # group or area list, csv file
        aList = []
        csvGroup = open(fileName + '.csv', 'r')
        csvReader = csv.reader(csvGroup)
        for item in csvReader:
            aList.append(item)
        return aList

    def addNewGroups(self,service, groupList):
        failed = []
        for aGroup in groupList:
            modifiedGroup = {'email':aGroup[0], 'name':aGroup[0][:3].upper() + ' Residents', 'description': ' Created By Yujia Shai Xie July 2017'}
            try:
                service.groups().insert(body=modifiedGroup).execute()
                print("Successfully Added: " + aGroup[0])
            except:
                print('Failed to insert group ' + str(aGroup) + ' Error Message: ', sys.exc_info()[1])
                failed.append(aGroup)
        return failed


    def addToAllGroups(self,service, userList, groupList):
        failed = []
        for aUser in userList:
            modifiedUser = {'email':aUser, 'role':'OWNER'}
            for aGroup in groupList:
                try:
                    service.members().insert(groupKey=aGroup[0], body=modifiedUser).execute()
                    print("Successfully Added: " + aUser + ' to group ' + str(aGroup[0]))
                except:
                    print('Failed to add user ' + aUser + ' to group ' + str(aGroup[0]) + ' Error Message: ' , sys.exc_info()[1])
                    temp = {'email':aUser, 'emailGroup':aGroup[0]}
                    failed.append(temp)  
        return failed

    def addAllAccess(self,service, userList, groupList): ## not using
        failed = []
        for aUser in userList:
            modifiedUser = {'email':aUser, 'role':'OWNER'}
            for aGroup in groupList:
                try:
                    service.members().update(groupKey=aGroup, memberKey=aUser, body=modifiedUser).execute()
                except:
                    print('Failed to update user ' + aUser + ' to group' + str(aGroup) + ' Error Message: ' , sys.exc_info()[1])
                    temp = {'email': aUser, 'emailGroup':aGroup}
                    failed.append(temp)
        return failed    

    def updateToGroup(self,service, userList, aRole):
        failed = []
        for aUser in userList:
            modifiedUser = {'email':aUser['email'], 'role':aRole}
            try:
                service.members().update(groupKey=aUser['emailGroup'], body=modifiedUser).execute()
            except:
                print('Failed to update user ' + aUser + ' as OWNER to group ' + aUser['emailGroup'] + ' Error Message: ' , sys.exc_info()[1])
                failed.append(aUser)
        return failed

    def addToGroup(self,service, userList, aRole):
        failed = []
        for aUser in userList:
            modifiedUser = {'email':aUser['email'], 'role': aRole}
            try:
                service.members().insert(groupKey=aUser['emailGroup'], body=modifiedUser).execute()
            except:
                print('Failed to add user ' + aUser['email'] + ' to group ' + aUser['emailGroup'] + ' Error Message: ' , sys.exc_info()[1])
                failed.append(aUser)
            # finally:
            #     count = count + 1
            #     print(str(count) + ' processed')
        return failed

    def addToGroupByArea(self,service, userList, aRole, aArea):
        failed = []
        for aUser in userList:
            if aArea == aUser['area']:
                modifiedUser = {'email':aUser['email'], 'role': aRole}
                try:
                    service.members().insert(groupKey=aUser['emailGroup'], body=modifiedUser).execute()
                    self.log('info', 'Successfully Added user ' + aUser['email'] + ' to group ' + aUser['emailGroup'])
                except:
                    print('Failed to add user ' + aUser['email'] + ' to group ' + aUser['emailGroup'] + ' Error Message: ' , sys.exc_info()[1])
                    self.log('debug', 'Failed to add user ' + aUser['email'] + ' to group ' + aUser['emailGroup'] + ' Error Message: ' + str(sys.exc_info()[1]))
                    failed.append(aUser)
                # finally:
                #     count = count + 1
                #     print(str(count) + ' processed')
        return failed

    def addGroupToSuperGroup(self, service, groupList, superGroup, aRole):
        failed = []
        for aGroup in groupList:
            modifiedGroup = {'email':aGroup[0], 'role':aRole}
            try:
                service.members().insert(groupKey=superGroup, body=modifiedGroup).execute()
                self.log('info', 'Successfully Added group ' + aGroup[0] + ' to supergroup ' + superGroup)
            except:
                print('Failed to add group ' + aGroup[0] + ' to supergroup ' + superGroup + ' Error Message: ', sys.exc_info()[1])
                self.log('debug', 'Failed to add group ' + aGroup[0] + ' to supergroup ' + superGroup + ' Error Message: ' + str(sys.exc_info()[1]))
                failed.append(aGroup[0])
        return failed

    def writeToFailedList(self, failList):
        with open('failed.csv', 'wb') as failedFile:
            csvWriter = csv.writer(failedFile)
            for aFiled in failList:
                csvWriter.writerow([aFiled])

    def log(self, logType, message):
        logging.basicConfig(filename='info.log', level=logging.DEBUG)
        if logType == 'debug':
            logging.debug(message)
        elif logType == 'info':
            logging.info(message)

    #def updateAccountInfo(self, info):

    def createUsers(self, service, users):
        failed = []
        for aUser in users:
            try:
                service.users().insert(aUser).execute()
                self.log('info', 'Successfully Created User ' + aUser['FirstName'] + ' ' + aUser['LastName'] + ' ' + aUser['email'])
            except:
                self.log('debug', 'Failed to Create User ' + aUser['FirstName'] + ' ' + aUser['LastName'] + ' ' + aUser['email'])
                failed.append(aUser)
        return failed

##########################################################################################################################################
app = RHAdmin()

credentials = app.get_credentials()
http = credentials.authorize(httplib2.Http())
service = discovery.build('admin', 'directory_v1', http=http)

groupList = app.getList('group')
userList = ['president@rha.gatech.edu', 'dia@rha.gatech.edu', 'advisor@rha.gatech.edu', 'it@rha.gatech.edu']
residentsList = app.get_resident_json('FallListV0')
summerGlennList = app.get_resident_json('SummerListUpdated')
# areaList = app.getList('area')

########## Delete corresponding email groups from the Admin Counsel

########## Create all groups
# print("CREATING ALL GROUPS")
# failedList = app.addNewGroups(service, groupList)


########## Adding President, DIA, IT, Advisor to ALL groups as OWNER
# print("ADDING PRESIDENT, DIA, IT, ADVISOR TO ALL GROUPS")
# failedList = app.addToAllGroups(service, userList, groupList)
# print(failedList)

########## Adding residents to the corresponding groups by area (too many residents...don't want to crash my laptop)
print("ADDING Residents to their corresponding groups")
failedList = app.addToGroupByArea(service, residentsList, "MEMBER", 'grad/fam')
print(failedList)

########## Adding all residents in the list
# print("ADDING Residents to the List")
# failedList = app.addToGroup(service, summerGlennList, "MEMBER")
# print(failedList)

########## Adding groups to superGroups
# print("ADDING Groups to Super Groups")
# superGroup = "residents@rha.gatech.edu" # all residents
# failedList = app.addGroupToSuperGroup(service, groupList, superGroup, "MEMBER")
# print(failedList)