#!/usr/bin/env python
#-*- coding: utf-8 -*-

from models import SurveyLine
import xlsxwriter

def exportSurvey(ModelClass, outFileName):

	dataContainer = []
	collectData(ModelClass, dataContainer)

	writeXlsx(dataContainer, outFileName)

##################################################################
##################################################################
## Essentially uses reflection to get column names and data from 
## a django model. Not tested to work on any model under the
## sun, but is successful for the ones used in this app.
##
## Works recursively to get related tables as well.
##
## Data container is a list of tuples in the following format:
##
## 	("className", ["header1", "header2", "header3"], ["val1", "val2", "val3"])
##
## Each tuple is a model (SQL table), which in the writeXlsx() function below
## will be exported to an excel worksheet.
def collectData(ModelClass, dataContainer=[], fkId=None, fkName=None):

	className = ModelClass().__class__.__name__
	fields = ModelClass._meta.fields

	header = [x.name for x in fields]
	data = []
	
	allEntries = list(ModelClass.objects.values())
	for entry in allEntries:
		row = []
		for f in fields:

			if f.is_relation:

				relFields = f.resolve_related_fields().pop(0)
				toJoin = [x.name for x in relFields]
				fName = "_".join(toJoin)
				
			else:
				fName = f.name
			fType = f.get_internal_type()

			obs = entry[fName]

			if fType == "NullBooleanField":
				if obs == True:
					obs = 1
				elif obs == False:
					obs = 0
				elif obs == None:
					obs = "NA"	
			
			elif fType == 'DateTimeField':

				obs = obs.strftime("%Y/%m/%d %H:%M:%S")

			row.append(obs)

		data.append(row)

	dataContainer.append((className, header, data))

	for relObj in ModelClass._meta.related_objects:

		RelMod = relObj.related_model
		collectData(RelMod, dataContainer)

	return

def writeXlsx(data, outFileName):

	workbook = xlsxwriter.Workbook(outFileName)
	
	try:
		for ws in data:
			wsName = ws[0]
			wsHeader = ws[1]
			wsData = ws[2]

			wsData.insert(0, wsHeader)

			worksheet = workbook.add_worksheet(wsName)

			for rowNum in range(0, len(wsData)):
				row = wsData[rowNum]
				for colNum in range(0, len(row)):
					worksheet.write(rowNum, colNum, wsData[rowNum][colNum])
					
	# Note that if there is an exception in this 
	# finally clause, any exception above in the
	# try clause will be lost
	finally:
		workbook.close()
