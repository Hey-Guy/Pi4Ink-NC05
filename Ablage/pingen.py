import os
hostname = "192.168.1.250" #example
response = os.system("ping -c 1 " + hostname)

#and then check the response...
if response == 0:
    print (hostname, 'is up!')
else:
    print (hostname, 'is down!')

### snip ###
import urllib.parse
import urllib.request

query='/iolinkmaster/port[1]/iolinkdevice/pdin/getdata'
enc_uri = urllib.parse.quote(query)
print("http://192.168.1.250/%s" % enc_uri) ### End

