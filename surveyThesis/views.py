#!/usr/bin/env python
#-*- coding: utf-8 -*-

from django.shortcuts import render
from forms import PageOne
from models import SurveyLine
import logging
from surveyThesis.constants import LANGUAGE_CHOICES, NATIVE_LANGUAGE_LABEL, ADD_LANGUAGE_BUTTON_TEXT, REMOVE_BUTTON_TEXT, FIELD_REQUIRED_MESS, VISION_DIFFICULTIES_TEXT, READING_DIFFICULTIES_TEXT

logger = logging.getLogger(__name__)

def surveyPage(request):

	logger.info('Testing with one page for now')	

	if request.method == 'POST':
		logger.info("Page was posted")
		form = PageOne(request.POST)

		if form.is_valid():
			logger.info('Add code to process data')
			data = form.cleaned_data
			surveyLine = SurveyLine(
				participantNumber=data['participantNumber'],
				age=data['age'],
				education=data['education'],
				undergradLevel=data['undergradLevel'],
				nativeLanguages=data['nativeLanguages'],
				)

			surveyLine.save()
		else: 
			logger.info('Form is not valid for some reason')

	else:
		form = PageOne()

	argsDict = {'form': form, 
			'langChoices': LANGUAGE_CHOICES,
			'natLangLabel': NATIVE_LANGUAGE_LABEL,
			'addLangButtonText': ADD_LANGUAGE_BUTTON_TEXT,
			'removeButtonText': REMOVE_BUTTON_TEXT,
			'natLangRequiredMess': FIELD_REQUIRED_MESS,
			}
	return render(request, 'one.html', argsDict)
