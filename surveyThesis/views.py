#!/usr/bin/env python
#-*- coding: utf-8 -*-

from django.shortcuts import render
from forms import PageOne, NativeLangForm, ForeignLangForm, BaseLangFormSet
from django.forms import formset_factory
from models import SurveyLine, NativeLangLine, ForeignLangLine
import logging
from surveyThesis.constants import LANGUAGE_CHOICES

logger = logging.getLogger(__name__)

def surveyPage(request):

	NatLangFormset = formset_factory(
						NativeLangForm, 
						min_num=1,
						validate_min=True, 
						extra=0,
						can_delete=True,
						formset=BaseLangFormSet,
	)
	ForLangFormset = formset_factory(
						ForeignLangForm,
						can_delete=True,
						formset=BaseLangFormSet,
	)

	if request.method == 'POST':

		form = PageOne(request.POST)
		natLangsForms = NatLangFormset(request.POST, request.FILES, prefix=u"natLang")
		forLangsForms = ForLangFormset(request.POST, request.FILES, prefix=u"forLang")


		mainFormValid = form.is_valid()
		# see if the foreign languages were visible and need validation
		forLangBoolVal = form.cleaned_data.get("foreignLangBool")
		#if forLangBoolVal == u"False":
		#	forLangBoolVal = False
		#elif forLangBoolVal == u"True":
		#	forLangBoolVal = True
		#else:
		#	forLangBoolVal = bool(forLangBoolVal)

		if not forLangBoolVal:
			for flf in forLangsForms:
				flf.needsValidation = False

		natLangsValid = natLangsForms.is_valid()
		forLangsValid = forLangsForms.is_valid()

		if not forLangBoolVal:
			# post is valid but we won't be saving any data for it
			forLangsValid = True

		if mainFormValid and natLangsValid and forLangsValid:
			data = form.cleaned_data
			import pdb; pdb.set_trace()
			surveyLine = SurveyLine(
				participantNumber=data['participantNumber'],
				age=data['age'],
				gender=data["gender"],
				education=data['education'],
				undergradLevel=data['undergradLevel'],
				visionProblems=data['visionProblems'],
				visionProblemsDetails=data['visionProblemsDetails'],
				hearingProblems=data['hearingProblems'],
				hearingProblemsDetails=data['hearingProblemsDetails'],
				foreignLangBool=data['foreignLangBool'],
				)
			surveyLine.save()

			for natLangForm in natLangsForms:
				data = natLangForm.cleaned_data
				if not data["DELETE"]:
					natLangLine = NativeLangLine(
						surveyId=surveyLine,
						nativeLang=data["nativeLang"],
					)
					natLangLine.save()

			if forLangBoolVal:
				for forLangForm in forLangsForms:
					data = forLangForm.cleaned_data
					if not data["DELETE"]:
						forLangLine = ForeignLangLine(
							surveyId=surveyLine,
							foreignLang=data["foreignLang"],
							proficiency=data["proficiency"],
							school=data["school"],
							livedAbroad=data["lived"],
							worked=data["worked"],
							other=data["other"],
							schoolSemesters=forLangForm.schoolTotal,
							livedAbroadDays=forLangForm.livedTotal,
							workedDays=forLangForm.workedTotal,
							otherDays=forLangForm.otherTotal,
						)
						otherDesc = data.get("otherStudyExplanation")
						if otherDesc is not None:
							forLangLine.otherDescription = otherDesc

						forLangLine.save()


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
