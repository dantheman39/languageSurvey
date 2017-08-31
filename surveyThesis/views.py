#!/usr/bin/env python
#-*- coding: utf-8 -*-

from django.shortcuts import render
from forms import PageOne
from models import SurveyLine
import logging
from surveyThesis.constants import LANGUAGE_CHOICES

logger = logging.getLogger(__name__)

def surveyPage(request):

	logger.info('Testing with one page for now')	

	if request.method == 'POST':
		logger.info("Page was posted")
		form = PageOne(request.POST)

		if form.is_valid():
			logger.info('Add code to process data')
			data = form.cleaned_data
			#surveyLine = SurveyLine(
			#	participantNumber=data['participantNumber'],
			#	age=data['age'],
			#	education=data['education'],
			#	undergradLevel=data['undergradLevel'],
			#	nativeLanguages=data['nativeLanguages'],
			#	)

			#surveyLine.save()
		else: 
			logger.info('Form is not valid for some reason')

	else:
		form = PageOne()

	argsDict = {'form': form, 
			}
	return render(request, 'one.html', argsDict)
