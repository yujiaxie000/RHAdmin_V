from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import httplib2
import json

# Email of the Service Account
SERVICE_ACCOUNT_EMAIL = 'rha-dia-yxie-1718@yujia-xie1718.iam.gserviceaccount.com'

# Path to the Service Account's Private Key file
SERVICE_ACCOUNT_PKCS12_FILE_PATH = 'RHA-DIA-1718-Server2.p12'

# Scope of this script
SCOPE = ['https://www.googleapis.com/auth/admin.directory.group','https://www.googleapis.com/auth/admin.directory.user',
'https://www.googleapis.com/auth/admin.directory.domain','https://www.googleapis.com/auth/admin.directory.resource.calendar',
'https://www.googleapis.com/auth/admin.directory.customer', 'https://www.googleapis.com/auth/admin.directory.userschema'
]

def create_directory_service(user_email):
    """Build and returns an Admin SDK Directory service object authorized with the service accounts
    that act on behalf of the given user.

    Args:
      user_email: The email of the user. Needs permissions to access the Admin APIs.
    Returns:
      Admin SDK directory service object.
    """

    credentials = ServiceAccountCredentials.from_p12_keyfile(SERVICE_ACCOUNT_EMAIL,
        SERVICE_ACCOUNT_PKCS12_FILE_PATH,
        'notasecret',
        SCOPE)
    #credentials = credentials.create_delegated(user_email)
    http = credentials.authorize(httplib2.Http())

    return build('admin', 'directory_v1', credentials=credentials)

def main():
    service = create_directory_service('dia@rha.gatech.edu')
    response = service.groups().get(groupKey='wdf.summer.residents@rha.gatech.edu').execute()

    # print(json.dumps(response, sort_keys=True, indent=4))
    print(response)

if __name__ == '__main__':
    credentials = ServiceAccountCredentials.from_json_keyfile_name('RHA-DIA-1718-Server2.json', SCOPE)
    credentials = credentials.create_delegated('dia@rha.gatech.edu')
    service = build('admin', 'directory_v1', credentials=credentials)
    print(service)
    print(service.groups())
    print(service.groups().get(groupKey='wdf.summer.residents@rha.gatech.edu'))
    response = service.groups().get(groupKey='wdf.summer.residents@rha.gatech.edu').execute()