#!/usr/bin/env python
#-*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from forms import SurveyForm, NativeLangForm, HeritageLangForm, ForeignLangForm, BaseLangFormSet
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User as DjangoUser
from django.core.exceptions import ObjectDoesNotExist
from django.forms import formset_factory
from models import SurveyLine, NativeLangLine, ForeignLangLine, HeritageLangLine
import logging
from settings import ALLOW_RESUBMIT
from surveyThesis.constants import LANGUAGE_CHOICES
from export import exportSurvey as exS
import os
from django.http import HttpResponse

logger = logging.getLogger(__name__)

@login_required
def surveyPage(request):

	user = request.user
	isAdmin = user.is_staff or user.is_superuser

	try:
		entry = SurveyLine.objects.get(userName=user)
		# we already have an entry for this person
		if ALLOW_RESUBMIT:
			pass
		elif not isAdmin:
			return render(request, "alreadySubmitted.html")

	except ObjectDoesNotExist:
		pass

	request, template, argsDict = processSurvey(request, userName=user) 

	argsDict["user"] = user
	if isAdmin:
		argsDict["isAdmin"] = True

	return render(request, template, argsDict)


@staff_member_required
def results(request):

	usersDates = list(SurveyLine.objects.values_list("userName", "date", "id", "dateLastEdited"))
	
	argsDict = { 
		"usersDates": usersDates,
	}

	return  render(request, "results.html", argsDict)

@staff_member_required
def deleteEntry(request, surveyId):

	SurveyLine.objects.get(pk=surveyId).delete()
	usersDates = list(SurveyLine.objects.values_list("userName", "date", "id", "dateLastEdited"))

	argsDict = {
		"usersDates": usersDates,
	}

	return render(request, "entryList.html", argsDict)

@staff_member_required
def resultsViewOne(request, surveyId):

	request, template, argsDict = processSurvey(request, adminView=True, adminViewId=surveyId)

	forUser = SurveyLine.objects.get(id=surveyId).userName
	argsDict["resultsForUser"] = forUser

	return render(request, template, argsDict)

@staff_member_required
def exportSurvey(request):

	today = timezone.now().strftime("%Y-%m-%d")
	rootFolder = '/tmp'
	fileName = 'survey_' + today + '.xlsx'
	outName = os.path.join(rootFolder, fileName)
	exS(SurveyLine, outName)

	response = HttpResponse()
	response['Content-Disposition'] = 'attachment; filename={0}'.format(fileName)
	response['X-Sendfile'] = outName
		
	#return render(request, 'languageSurvey/resultsTest.html', {'userName': request.user})
	return response

def processSurvey(request, adminView=False, adminViewId=None, userName=None):

	NatLangFormset = formset_factory(
						NativeLangForm, 
						min_num=1,
						validate_min=True, 
						extra=0,
						can_delete=True,
						formset=BaseLangFormSet,
	)
	HerLangFormset = formset_factory(
						HeritageLangForm,
						can_delete=True,
						formset=BaseLangFormSet,
	)

	ForLangFormset = formset_factory(
						ForeignLangForm,
						can_delete=True,
						formset=BaseLangFormSet,
	)

	if request.method == 'POST':

		form = SurveyForm(request.POST)
		natLangsForms = NatLangFormset(request.POST, request.FILES, prefix=u"natLang")
		herLangsForms = HerLangFormset(request.POST, request.FILES, prefix=u"herLang")
		forLangsForms = ForLangFormset(request.POST, request.FILES, prefix=u"forLang")


		mainFormValid = form.is_valid()
		# see if the foreign languages were visible and need validation
		forLangBoolVal = form.cleaned_data.get("foreignLangBool")
		herLangBoolVal = form.cleaned_data.get("heritageLangBool")

		if not forLangBoolVal:
			for flf in forLangsForms:
				flf.needsValidation = False
		if not herLangBoolVal:
			for hlf in herLangsForms:
				hlf.needsValidation = False

		natLangsValid = natLangsForms.is_valid()
		forLangsValid = forLangsForms.is_valid()
		herLangsValid = herLangsForms.is_valid()

		if not forLangBoolVal:
			# post is valid but we won't be saving any data for it
			forLangsValid = True
		if not herLangBoolVal:
			herLangsValid = True

		if mainFormValid and natLangsValid and herLangsValid and forLangsValid:
			data = form.cleaned_data

			# see if admin is updating or if participant is posting new
			surveyLine = None
			try: 
				if adminView:
					surveyLine = SurveyLine.objects.get(id=adminViewId)
				else:
					surveyLine = SurveyLine.objects.get(userName=userName)
			except ObjectDoesNotExist:
				pass


			if surveyLine is not None:
				# we are updating a pre-existing entry

				# first is the model attribute, second is the form attribute
				attrs = [
					"age",
					"gender",
					"education",
					"undergradLevel",
					"foreignLangBool",
					"heritageLangBool",
					"visionProblems",
					"visionProblemsDetails",
					"hearingProblems",
					"hearingProblemsDetails",
				]

				for att in attrs:
					setattr(surveyLine, att, data[att])

				surveyLine.dateLastEdited = timezone.now()

				if adminView and "adminComment" in data:
					surveyLine.adminComment = data["adminComment"]

				# It's going to be easier to delete than to update
				nlEntry = surveyLine.nativelangline_set.all()
				hlEntry = surveyLine.heritagelangline_set.all()
				flEntry = surveyLine.foreignlangline_set.all()
				for lq in [nlEntry, hlEntry, flEntry]:
					for le in lq:
						le.delete()

				surveyLine.save()

			else:
				# we are creating a new entry
				surveyLine = SurveyLine(
					userName=request.user,
					date=timezone.now(),
					age=data['age'],
					gender=data["gender"],
					education=data['education'],
					undergradLevel=data['undergradLevel'],
					visionProblems=data['visionProblems'],
					visionProblemsDetails=data['visionProblemsDetails'],
					hearingProblems=data['hearingProblems'],
					hearingProblemsDetails=data['hearingProblemsDetails'],
					foreignLangBool=data['foreignLangBool'],
					heritageLangBool=data['heritageLangBool'],
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
							lived=data["lived"],
							worked=data["worked"],
							other=data["other"],
							schoolSemestersTotal=forLangForm.schoolTotal,
							livedDaysTotal=forLangForm.livedTotal,
							workedDaysTotal=forLangForm.workedTotal,
							otherDaysTotal=forLangForm.otherTotal,
							schoolSemesters=data["schoolSemesters"],
							schoolYears=data["schoolYears"],
							livedYears=data["livedYears"],
							workedYears=data["workedYears"],
							otherYears=data["otherYears"],
							livedMonths=data["livedMonths"],
							workedMonths=data["workedMonths"],
							otherMonths=data["otherMonths"],
							livedWeeks=data["livedWeeks"],
							workedWeeks=data["workedWeeks"],
							otherWeeks=data["otherWeeks"],
							livedDays=data["livedDays"],
							workedDays=data["workedDays"],
							otherDays=data["otherDays"],
						)
						otherDesc = data.get("otherStudyExplanation")
						if otherDesc is not None:
							forLangLine.otherDescription = otherDesc

						forLangLine.save()

			if herLangBoolVal:
				for herLangForm in herLangsForms:
					data = herLangForm.cleaned_data
					if not data["DELETE"]:
						herLangLine = HeritageLangLine(
							surveyId=surveyLine,
							heritageLang=data["heritageLang"],
							explanation=data["explanation"],
						)
						herLangLine.save()

			if adminView:
				compTemp = "editSuccessful.html"
			else:
				compTemp = "completed.html"
			return request, compTemp, {}

		else: 
			logger.info('Form is not valid')

	# the "if" before this was if == "POST"
	else:

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
				"adminComment": entry.adminComment,
				"age": entry.age, 
				"gender": entry.gender,
				"education": entry.education,
				"undergradLevel": entry.undergradLevel,
				"foreignLangBool": entry.foreignLangBool,
				"heritageLangBool": entry.heritageLangBool,
				"visionProblems": entry.visionProblems,
				"visionProblemsDetails": entry.visionProblemsDetails,
				"hearingProblems": entry.hearingProblems,
				"hearingProblemsDetails": entry.hearingProblemsDetails,
			
			}
			form = SurveyForm(initial=initial)

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
					"lived": fle.lived,
					"worked": fle.worked,
					"other": fle.other,
					"schoolSemesters": fle.schoolSemesters,
					"livedDays": fle.livedDays,
					"workedDays": fle.workedDays,
					"otherDays": fle.otherDays,
					"otherStudyExplanation": fle.otherDescription, 
					"schoolYears": fle.schoolYears,
					"livedYears": fle.livedYears,
					"workedYears": fle.workedYears,
					"otherYears": fle.otherYears,
					"livedMonths": fle.livedMonths,
					"workedMonths": fle.workedMonths,
					"otherMonths": fle.otherMonths,
					"livedWeeks": fle.livedWeeks,
					"workedWeeks": fle.workedWeeks,
					"otherWeeks": fle.otherWeeks,
					"livedDays": fle.livedDays,
					"workedDays": fle.workedDays,
					"otherDays": fle.otherDays,
				}	
				flInitials.append(flInitial)

			hles = entry.heritagelangline_set.all()
			hlInitials = []
			if hles:
				HerLangFormset = formset_factory(
									HeritageLangForm,
									can_delete=True,
									formset=BaseLangFormSet,
									extra=0,
				)
			hlInitials=[]
			for hle in hles:
				hlInitial = {
					"heritageLang": hle.heritageLang,
					"explanation": hle.explanation,
				}
				hlInitials.append(hlInitial)

			natLangsForms = NatLangFormset(prefix=u"natLang", initial=nlInitials)
			forLangsForms = ForLangFormset(prefix=u"forLang", initial=flInitials)
			herLangsForms = HerLangFormset(prefix=u"herLang", initial=hlInitials)

		# we have no entry, give them empty form
		else:
			form = SurveyForm()
			natLangsForms = NatLangFormset(prefix=u"natLang")
			herLangsForms = HerLangFormset(prefix=u"herLang")
			forLangsForms = ForLangFormset(prefix=u"forLang")

	argsDict = {
		'form': form, 
		'natLangsForms': natLangsForms,
		'herLangsForms': herLangsForms,
		'forLangsForms': forLangsForms,
	}

	return request, "survey.html", argsDict
