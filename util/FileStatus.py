import json


Fileinfos = open('file_infos.txt', '+a')
lines = Fileinfos.readlines()
if len(lines) > 0:
	jobIdInfo = json.loads(lines)
else:
	jobIdInfo = dict()
	

def writeJobInfo(jsonData):
	json.dumps(jsonData, Fileinfos)

class FileStatus():
	jobId = None
	dateUploaded = None
	dateTranscription = None
	filename = None
	filelength = None
	transcriptionCompleted = False
	transcriptionProgress = 0
	isTranscriptionEdited = False

	
	def __init__(self, jobId, filename, filelength, dateUploaded):
		self.jobId = jobId
		self.filename = filename
		self.filelength = filelength
		self.dateUploaded = dateUploaded



fileStatus = dict()
jobIdInfo = list()

def createJobIdFileInfo(jobId, filename, filelength, dateUploaded):
	#jobIdInfo[jobId] = FileStatus(jobId, filename, filelength, dateUploaded)
	#jobIdInfo[jobId] = fileInfo(filename, filelength, dateUploaded)
	fileStatus['filename'] = filename
	fileStatus['filelength'] = filelength
	fileStatus['dateUploaded'] = dateUploaded
	jobIdInfo[jobId] = fileStatus

def addTranscriptionProgress(jobId, transcriptionProgress):
	jobIdInfo[jobId].transcriptionProgress = transcriptionProgress
	fileStatus['transcriptionProgress'] = transcriptionProgress

def addDateTranscription(jobId, dateTranscription):
	jobIdInfo[jobId].dateTranscription = dateTranscription
	fileStatus['dateTranscription'] = dateTranscription

def addTranscriptionCompleted(jobId, transcriptionCompleted):
	jobIdInfo[jobId].transcriptionCompleted = transcriptionCompleted
	fileStatus['transcriptionCompleted'] = transcriptionCompleted

def addIsTranscriptionEdited(jobId, isTranscriptionEdited):
	jobIdInfo[jobId].isTranscriptionEdited = isTranscriptionEdited
	fileStatus['isTranscriptionEdited'] = isTranscriptionEdited

def getTranscriptionProgress(jobId):
	return jobIdInfo[jobId].transcriptionProgress

def checkTranscriptionCompleted(jobId):
	return jobIdInfo[jobId].transcriptionCompleted

def getFilename(jobId):
	return jobIdInfo[jobId].filename

def deleteJobIdInfo(jobId):
    # ---
	del jobIdInfo[jobId]

def cancelJob(jobId):
    return ''
