#!/usr/bin/env python
#-*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from forms import PageOne, NativeLangForm, ForeignLangForm, BaseLangFormSet
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User as DjangoUser
from django.core.exceptions import ObjectDoesNotExist
from django.forms import formset_factory
from models import SurveyLine, NativeLangLine, ForeignLangLine
import logging
from surveyThesis.constants import LANGUAGE_CHOICES

logger = logging.getLogger(__name__)

@login_required
def surveyPage(request):

	user = request.user

	request, argsDict = processSurvey(request, userName=user) 

	argsDict["user"] = user

	return render(request, 'one.html', argsDict)

def processSurvey(request, adminView=False, adminViewId=None, userName=None):

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
			surveyLine = SurveyLine(
				userName=request.user,
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

		
		#import pdb; pdb.set_trace()

		entry = None
		try:

			if adminView:
				entry = get_object_or_404(SurveyLine, id=adminViewId)
			else:
				# see if we have an entry in the database
				entry = SurveyLine.objects.get(userName=userName)

		except ObjectDoesNotExist:

			pass

		if entry is not None:

			initial = {
				"age": entry.age, 
				"gender": entry.gender,
				"education": entry.education,
				"undergradLevel": entry.undergradLevel,
				"foreignLangBool": entry.foreignLangBool,
				"visionProblems": entry.visionProblems,
				"visionProblemsDetails": entry.visionProblemsDetails,
				"hearingProblems": entry.hearingProblems,
				"hearingProblemsDetails": entry.hearingProblemsDetails,
			
			}
			form = PageOne(initial=initial)

			# nativeLangEntries
			nles = entry.nativelangline_set.all()
			nlInitials = []
			for nle in nles:
				nlInitial = {
					"nativeLang": nle.nativeLang,
				}
				nlInitials.append(nlInitial)
			# foreignLangEntries
			fles = entry.foreignlangline_set.all()

			if fles:
				# overwrite initial factory to set extra=0
				ForLangFormset = formset_factory(
									ForeignLangForm,
									can_delete=True,
									formset=BaseLangFormSet,
									extra=0,
				)

			flInitials=[]
			for fle in fles:
				flInitial = {
					"foreignLang": fle.foreignLang,
					"proficiency": fle.proficiency,
					"school": fle.school,
					"lived": fle.livedAbroad,
					"worked": fle.worked,
					"other": fle.other,
					"schoolSemesters": fle.schoolSemesters,
					"livedDays": fle.livedAbroadDays,
					"workedDays": fle.workedDays,
					"otherDays": fle.otherDays,
					"otherStudyExplanation": fle.otherDescription, 
				}	
				flInitials.append(flInitial)

			natLangsForms = NatLangFormset(prefix=u"natLang", initial=nlInitials)
			forLangsForms = ForLangFormset(prefix=u"forLang", initial=flInitials)

		# we have no entry, give them empty form
		else:
			form = PageOne()
			natLangsForms = NatLangFormset(prefix=u"natLang")
			forLangsForms = ForLangFormset(prefix=u"forLang")

	argsDict = {
		'form': form, 
		'natLangsForms': natLangsForms,
		'forLangsForms': forLangsForms,
	}

	return request, argsDict


@staff_member_required
def results(request):

	usersDates = list(SurveyLine.objects.values_list("userName", "date", "id"))
	
	argsDict = { 
		"usersDates": usersDates,
	}

	return  render(request, "results.html", argsDict)

@staff_member_required
def resultsViewOne(request, surveyId):

	request, argsDict = processSurvey(request, adminView=True, adminViewId=surveyId)

	forUser = SurveyLine.objects.get(id=surveyId).userName
	argsDict["resultsForUser"] = forUser

	return render(request, "one.html", argsDict)
