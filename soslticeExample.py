import sys
import requests
import random
from random import choice
true=1
false=0

#Solstice Pod config URL: IPAddress/api/config
#Solstice Pod stats URL: IPAddress/api/stats
#Solstice Pod control URL: IPAddress/api/control
#Solstice Pod calendar URL: IPAddress/api/calendar
#Solstice Pod config URL: IPAddress/api/version/
#Solstice Pod config URL: IPAddress/api/serial-passthru


newname = "New Name"
myurl = "http://192.168.3.227"
admin_password = ""
mystatsurl = myurl + "/api/stats"
myconfigurl = myurl + '/api/config'

rs=requests.get(mystatsurl)
rc=requests.get(myconfigurl)
rstats=eval(rs.text)
rconfig=eval(rc.text)

print("Current Display Name from Stats:")
rstats.get('m_displayInformation',{}).get('m_displayName')
print("Current Display Name from Config:")
rconfig.get('m_displayInformation',{}).get('m_displayName')

r=requests.post(myconfigurl, json=
{'password':'admin_password','m_displayInformation':
{'m_displayName':newname}})

print("Changing Name to: ", newname)
print("………….")

rs=requests.get(mystatsurl)
rc=requests.get(myconfigurl)
rstats=eval(rs.text)
rconfig=eval(rc.text)

print("New Display Name from Stats:")
rstats.get('m_displayInformation',{}).get('m_displayName')
print("New Display Name from Config:");
rconfig.get('m_displayInformation',{}).get('m_displayName')