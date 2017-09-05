#!/usr/bin/env python
#-*- coding: utf-8 -*-

from models import SurveyLine
import xlsxwriter

def exportSurvey(outFileName):

	allEntries = list(SurveyLine.objects.values())

	import pdb; pdb.set_trace()

	fields = SurveyLine._meta.fields
	#print(fields)

	header = [unicode(x.name) for x in fields]
	data = []
	data.append(header)

	for entry in allEntries:

		userRow = []

		for f in fields:
			
			fName = f.name
			fType = f.get_internal_type()
			
			obs = entry[fName]	

			if fType == 'NullBooleanField':

				if obs == True:
					obs = 1
				elif obs == False:
					obs = 0
				elif obs == None:
					obs = "NA"	
			
			elif fType == 'DateTimeField':

				obs = obs.strftime("%Y/%m/%d %H:%M:%S")

			userRow.append(obs)

		data.append(userRow)

	writeXlsx(data, outFileName)
	#print(data)

#data is a two dimensional tuple or list 
def writeXlsx(data, outFileName):

	workbook = xlsxwriter.Workbook(outFileName)
	worksheet = workbook.add_worksheet()

	try:
		for rowNum in range(0, len(data)):
			row = data[rowNum]
			for colNum in range(0, len(row)):
				worksheet.write(rowNum, colNum, data[rowNum][colNum])
			
	finally:
		workbook.close()
