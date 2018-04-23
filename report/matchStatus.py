# https://stackoverflow.com/questions/5458048/how-to-make-a-python-script-standalone-executable-to-run-without-any-dependency



import os, sys, re

statusPattern = """<TR><TD(.*?)Result Status:(.*?)(\w+)</FONT></TD></TR>"""

def readReport(filepath):
	file_handle = open(filepath, "r")
	text = file_handle.read()
	file_handle.close()
	return text	

def getStatus(status, text):
	result = re.search(status, text, re.S).group(3)		
	return result.upper()

def logStatus(filepath, summary):
	file_handle = open(filepath, "w")
	file_handle.write(summary)
	file_handle.close()
	return	

	
location = r"C:\Users\bilsto1\python\Utilities\exfo\report"
location = r"C:\Users\bilsto1\Desktop\Briefcase\Automation\AutomationResults\GVXAA-2018-04-18-GA-1.22.0.33-SN881665"


# If data subdirectory exists, it will save result file to output folder
# otherwise it save result to working directory
#location = os.getcwd() + ("\\data" if os.path.isdir("data") else "")


if os.path.isdir("data"):
	location = os.getcwd() + "\\data" 
	logPath = os.getcwd() + "\\output\\" 
else:
	location = os.getcwd()
	logPath = os.getcwd() + "\\"


for root, subdirs, files in os.walk(location):
	if root == location or 'archive' in root:
		continue

	automationList = [root]
	for index, file in enumerate(files):
		filenamepath = os.path.join(root, file)
		report = readReport(filenamepath)
		record = str(index+1)+","+getStatus(statusPattern, report)+","+file
		automationList.append(record)
	outcome = "\n".join(automationList)		
	logStatus(logPath + "log-"+root.split('\\')[-1]+".csv", outcome)	


