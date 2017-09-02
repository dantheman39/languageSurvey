#!/usr/bin/env python
#-*- coding: utf-8 -*-

from django.shortcuts import render
from forms import PageOne, NativeLangForm, ForeignLangForm
from django.forms import formset_factory
from models import SurveyLine
import logging
from surveyThesis.constants import LANGUAGE_CHOICES

logger = logging.getLogger(__name__)

def surveyPage(request):

	logger.info('Testing with one page for now')	
	NatLangFormset = formset_factory(
						NativeLangForm, 
						min_num=1,
						validate_min=True, 
						extra=0,
						can_delete=True,
	)
	ForLangFormset = formset_factory(
						ForeignLangForm,
						can_delete=True,
	)

	if request.method == 'POST':
		logger.info("Page was posted")
		form = PageOne(request.POST)
		natLangsForms = NatLangFormset(request.POST, request.FILES, prefix=u"natLang")
		forLangsForms = ForLangFormset(request.POST, request.FILES, prefix=u"forLang")

		# for debugging
		for ke, va in request.POST.iteritems():
			if ke[:4] == "natL":
				print("{0}\t{1}".format(ke,va))
		natLangsForms.is_valid()
		for natLangForm in natLangsForms:
			print("Form")
			print(natLangForm.cleaned_data)

		if form.is_valid() and natLangsForms.is_valid():
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
		natLangsForms = NatLangFormset(prefix=u"natLang")
		forLangsForms = ForLangFormset(prefix=u"forLang")

	argsDict = {
		'form': form, 
		'natLangsForms': natLangsForms,
		'forLangsForms': forLangsForms,
	}
	return render(request, 'one.html', argsDict)
