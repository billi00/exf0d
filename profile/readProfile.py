# https://stackoverflow.com/questions/5458048/how-to-make-a-python-script-standalone-executable-to-run-without-any-dependency


import os, sys, re


pingPattern = """<AutoTestSetupValues>.*?<Ping>(.*?)</Ping>.*?<PingURL>(.*?)</PingURL>.*?<PingAddress>(.*?)</PingAddress>.*?<PingAddressFormat>(.*?)</PingAddressFormat>.*?</AutoTestSetupValues>"""

temp = """
<AutoTestSetupValues>
<Ping>Enable</Ping>
    <PingURL>www.google.ca</PingURL>
    <PingAddress>199.166.16.247</PingAddress>
    <PingIPv6Address>2607:f8b0:400b:806::2004</PingIPv6Address>
    <PingAddressFormat>IPAddress</PingAddressFormat>
    <PingMaxHops>32</PingMaxHops>
    <PingPacketSize>32</PingPacketSize>
    <PingTimeout>1</PingTimeout>
    <PingTotalPings>10</PingTotalPings>
    </OoklaServerList>
  </AutoTestSetupValues>
  <EthernetTestSetupValues>
"""



testTags = """
Ping
PingAddressFormat
PingURL
PingAddress

FTP
<FTPTestSetup>
FTPAddressFormat
FileUpload
FileDownload
FTPServerIPAddress
IPAddressUserName
IPAddressPassword
IPAddressDownloadFile
IPAddressUploadFile
IPAddressUploadFileSize
FTPServerURL
URLUserName
URLPassword
URLDownloadFile
URLUploadFile
URLUploadFileSize
UploadSessions
DownloadSessions

HTTP
<HTTPTestSetup>
HTTPServerAddress
DownloadSessions

SpeedTest
<SpeedTestSetup>
TestType
iperfAddressFormat
iperfUpload
iperfDownload
iperfServerIPAddress
iperfServerURL
iperfUploadSessions
iperfDownloadSessions
ooklaServer

Traceroute
TraceRouteURL
TraceRouteAddress
TraceRouteAddressFormat

IPTVtest

VOIPtest
<VOIPTestSetup>
CodecType
AddressFormat
ProxyServerURL
ProxyServerAddr


"""

optionaltags = """
LineMode
SyncTimePeriod
SyncLossCounter
AccessMode
WanVlanSupport
WanVlanId
WanLoginTimeout
Igmpver
WanIpObtainIp
WanIpStaticIp
WanIpLoginName
WanIpPassword
StaticVerifyGateway
IPOAVerifyGateway
BondingThreshold
MinSnrMarginDn
MinSnrMarginUp
MaxAttenuationDn
MaxAttenuationUp
LanPassThroughMode
KeepPowerOn
"""


allTags = """Ping
PingAddressFormat
PingURL
PingAddress
FTP
FTPAddressFormat
FileUpload
FileDownload
FTPServerIPAddress
IPAddressUserName
IPAddressPassword
IPAddressDownloadFile
IPAddressUploadFile
IPAddressUploadFileSize
FTPServerURL
URLUserName
URLPassword
URLDownloadFile
URLUploadFile
URLUploadFileSize
UploadSessions
HTTP
HTTPServerAddress
SpeedTest
TestType
iperfAddressFormat
iperfUpload
iperfDownload
iperfServerIPAddress
iperfServerURL
iperfUploadSessions
iperfDownloadSessions
ooklaServer
Traceroute
TraceRouteURL
TraceRouteAddress
TraceRouteAddressFormat
IPTVtest
VOIPtest
CodecType
AddressFormat
ProxyServerURL
ProxyServerAddr
LineMode
SyncTimePeriod
SyncLossCounter
AccessMode
WanVlanSupport
WanVlanId
WanLoginTimeout
Igmpver
WanIpObtainIp
WanIpStaticIp
WanIpLoginName
WanIpPassword
StaticVerifyGateway
IPOAVerifyGateway
BondingThreshold
MinSnrMarginDn
MinSnrMarginUp
MaxAttenuationDn
MaxAttenuationUp
LanPassThroughMode
KeepPowerOn
"""



def readProfile(filepath):
	file_handle = open(filepath, "r")
	text = file_handle.read()
	file_handle.close()
	return text	

	
def getPattern(tag):
	return r'<AutoTestSetupValues>.*?<'+tag+r'>(.*?)</'+tag+r'>'


def getValue(pattern, text):
	result = re.search(pattern, text, re.S)
	try:
		return result.group(1)
	except:
		return "N/A"
	#return re.search(pattern, text, re.S).group(1)
	

def logTestGrid(filepath, summary):
	file_handle = open(filepath, "w")
	file_handle.write(summary)
	file_handle.close()
	return	



tagList = allTags.split()

patternList = []

for tag in tagList:
	patternList.append(getPattern(tag))
"""
# test patternList
for index, item in enumerate(patternList):
	print (index, item)
"""
	

# If data subdirectory exists, it will save result file to output folder
# otherwise it save result to working directory
location = os.getcwd() + ("\\output" if os.path.isdir("data") else "")

outcome = ""

header = "Old Order, Filename, " + ", ".join(tagList)

logName = ""


for root, subdirs, files in os.walk(location):
	if root == location:
		logName = "log-"+root.split('\\')[-1]+".csv"
		print(logName)
		continue

	automationList = [root, header]
	for index, file in enumerate(files):
		filenamepath = os.path.join(root, file)
		report = readProfile(filenamepath)
		#record = str(index+1) + ", "+file + ", "+ getValue(pingPattern, report)
		record = str(index+1) + ", " + file
		for pat in patternList:
			record +=  ", "+ getValue(pat, report)
		
		automationList.append(record)
	outcome += "\n".join(automationList) +"\n"
logName = location + "\\" + logName
print(logName)
logTestGrid(logName, outcome)	

