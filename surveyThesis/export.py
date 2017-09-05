#!/usr/bin/env python
#-*- coding: utf-8 -*-

from models import SurveyLine
import xlsxwriter

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

def exportSurvey(ModelClass, outFileName):

	dataContainer = []
	collectData(ModelClass, dataContainer)

	writeXlsx(dataContainer, outFileName)

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
					
	finally:
		workbook.close()
