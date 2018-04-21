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



for root, subdirs, files in os.walk(location):
	if root == location:
		continue

	automationList = [root]
	for index, file in enumerate(files):
		filenamepath = os.path.join(root, file)
		report = readReport(filenamepath)
		record = str(index+1)+","+getStatus(statusPattern, report)+","+file
		automationList.append(record)
	outcome = "\n".join(automationList)		
	logStatus("log-"+root.split('\\')[-1]+".csv", outcome)	
	print(outcome)
