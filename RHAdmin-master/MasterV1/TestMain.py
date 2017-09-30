# from RHAdmin.RHAdmin_V01 import RHAdmin_V01 as ad

# test = ad('RHA-DIA-1718-Client.json', 'Client for rha-dia-1718')
# service = test.authenticate()

# users = []
# users.append({'primaryEmail':'test01@rha.gatech.edu', 'password': 'rha.test', 'name':{'familyName': 'A', 'givenName': 'RHA'}})
# users.append({'primaryEmail':'test02@rha.gatech.edu', 'password': 'rha.test', 'name':{'familyName': 'B', 'givenName': 'RHA'}})


# failed = test.createUsers(service, users)


from RHAdmin.FormatConvertor_V01 import FormatConvertor as fc 

test = fc()
temp = test.convert_byArea('roster.csv', 1)

print(temp)