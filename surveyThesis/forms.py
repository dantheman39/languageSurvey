#!/usr/bin/env python
#-*- coding: utf-8 -*-

from django import forms
from django.forms import BaseFormSet
from django.utils.translation import ugettext as _
from surveyThesis.models import SurveyLine, ForeignLangLine
from surveyThesis.constants import ED_CHOICES, UG_CHOICES, LANGUAGE_CHOICES, YES_NO_CHOICES, PROFICIENCY_CHOICES, GENDER_CHOICES
import logging

logger = logging.getLogger('surveyThesis')
FIELD_REQUIRED_MESS = _(u"This field is required")
SORTOF_OPTIONAL = _(u"If you don't want to answer, you can say so here, but this field can't be blank")

class PageOne(forms.Form):

	pageTitle = _(u"Language background survey")
	
	genderLabel = _(u"Gender")

	nativeLanguageLabel = _(u"Native language")
	nativeLangLegend = _(u"Native language(s)")

	addLanguageButtonText = _(u"Add another")
	removeButtonText = _(u"Remove")
	addForLangText = _(u"Add foreign language")
	rmForLangText = _(u"Remove")

	visionProblemsText = _(u"Do you have any vision or reading problems?")
	visionProblemsDetailsText = _(u"If you are comfortable doing so, please explain.")

	hearingProblemsText = _(u"Do you have any hearing problems?")
	hearingProblemsDetailsText = visionProblemsDetailsText

	undergradBlankError = _(u"Please tell us what year you are in, or the last year you completed")

	foreignLangsQuestion = _(u"Do you speak, or have you studied a foreign language?")

	adminComment = forms.CharField(
				required=False,
				widget = forms.Textarea,
				)


	age = forms.IntegerField(label=_(u'Age'),
				label_suffix='',
				error_messages={'required': FIELD_REQUIRED_MESS},
				#localize=True,
				)
	gender = forms.ChoiceField(label=_(u"Gender"),
				label_suffix='',
				error_messages={'required': FIELD_REQUIRED_MESS},
				choices=GENDER_CHOICES,
				)
	education = forms.ChoiceField(label=_(u'Current education level'),
				label_suffix='',
				error_messages={'required': FIELD_REQUIRED_MESS},
				choices=ED_CHOICES,
				)

	undergradLevel = forms.ChoiceField(label=_(u'Undergrad level'),
				label_suffix='',
				error_messages={'required': FIELD_REQUIRED_MESS},
				choices=UG_CHOICES,
				required=False,
				)

	#nativeLanguages = forms.CharField(
	#			max_length=200,
	#			)

	visionProblems = forms.ChoiceField(
				choices=YES_NO_CHOICES,
				widget=forms.RadioSelect,
				)

	visionProblemsDetails = forms.CharField(
				required=False,
				widget = forms.Textarea,
				error_messages={'required': SORTOF_OPTIONAL},
				)

	hearingProblems = forms.ChoiceField(
				choices=YES_NO_CHOICES,
				widget=forms.RadioSelect,
				)

	hearingProblemsDetails = forms.CharField(
				required=False,
				widget = forms.Textarea,
				error_messages={'required': SORTOF_OPTIONAL},
				)

	#foreignLanguages = forms.CharField(
	#			widget = forms.Textarea,
	#			)

	foreignLangBool = forms.ChoiceField(
				choices=YES_NO_CHOICES,
				widget=forms.RadioSelect,
				)

	foreignProficiencyChoices = PROFICIENCY_CHOICES 

	def castBooleanText(self, boolFields, cleaned_data):

		for bf in boolFields:
			bv = cleaned_data.get(bf)
			if bv is not None:
				if bv == "True":
					bv = True
				elif bv == "False":
					bv = False

				cleaned_data[bf] = bv

	def clean(self):
		cleaned_data = super(PageOne, self).clean()

		# for some reason radio buttons are not being
		# correctly converted to python types
		boolFields = [
			"visionProblems",
			"hearingProblems",
			"foreignLangBool",
		]
		self.castBooleanText(boolFields, cleaned_data)
				

		if 'education' in cleaned_data:
			educationSelection = cleaned_data.get('education')
			if educationSelection == "undergrad":
				if 'undergradLevel' not in cleaned_data or not cleaned_data['undergradLevel']:
					valError = forms.ValidationError(self.undergradBlankError)
					self.add_error('undergradLevel', valError)

		checkBox_description = [
			("visionProblems", "visionProblemsDetails"),
			("hearingProblems", "hearingProblemsDetails"),
		]

		for cdt in checkBox_description:
			checkName = cdt[0]
			descName = cdt[1]
			if checkName in cleaned_data:
				checked = cleaned_data.get(checkName)
				if checked == True:
					description = cleaned_data.get(descName)
					if not description:
						valError = forms.ValidationError(SORTOF_OPTIONAL)
						self.add_error(descName, valError)
				else:
					# make sure the descriptino is blank.
					# If they change their mind and uncheck 
					# it, we don't want to save their description
					cleaned_data[descName] = u""


		return cleaned_data

class NativeLangForm(forms.Form):

	# this will be used by the BaseLangFormSet to 
	# check for duplicate languages
	langFieldName = "nativeLang"

	nativeLang = forms.ChoiceField(label=_(u'Native language'),
				label_suffix='',
				error_messages={'required': FIELD_REQUIRED_MESS},
				choices=LANGUAGE_CHOICES,
				)

class ForeignLangForm(forms.Form):

	# this will be used by the BaseLangFormSet to 
	# check for duplicate languages
	langFieldName = "foreignLang"

	foreignLangLabel = _(u"Which one?")
	foreignLang = forms.ChoiceField(
					label=foreignLangLabel,
					label_suffix='',
					error_messages={'required': FIELD_REQUIRED_MESS},
					choices=LANGUAGE_CHOICES,
					required=False,
				)

	foreignProfLabel = _(u"Estimated proficiency")
	proficiency = forms.ChoiceField(
					label=foreignProfLabel,
					label_suffix='',
					error_messages={'required': FIELD_REQUIRED_MESS},
					choices=PROFICIENCY_CHOICES,
					required=False,
				)

	methodOfStudyQuestion = _(u"How did you learn or use it? (Check all that apply)")
	yearsText = _(u"Years")
	monthsText = _(u"Months")
	weeksText = _(u"Weeks")
	daysText = _(u"Days")
	daysTotalText = _(u"days total")
	livedQuestion = _(u"About how long were you there?")
	semestersQuestion = _(u"About how many semesters did you study for? (one semester is about 5 months, one year is two semesters) ")
	semestersText = _(u"Semesters")
	semestersTotalText = _(u"Semesters total")

	studyAttrs = { "class": "studyTime", "min": "0" }
	timeAttrs = { "class": "timeInput", "min": "0" }
	hideShowAttrs = { "class": "hideShowCb" }

	school = forms.BooleanField(label=_(u"Classes"), required=False)
	schoolSemesters = forms.IntegerField(
						label=semestersText, 
						initial=0, 
						required=False,
	)
	schoolSemesters.widget.attrs = studyAttrs

	schoolYears = forms.IntegerField(
						label=yearsText, 
						initial=0, 
						required=False,
	)
	schoolYears.widget.attrs = studyAttrs

	lived = forms.BooleanField(label=_(u"Lived"), required=False)
	livedYears = forms.IntegerField(
						label=yearsText, 
						initial=0, 
						required=False
	)
	livedMonths = forms.IntegerField(
						label=monthsText, 
						initial=0, 
						required=False
	)
	livedWeeks = forms.IntegerField(
						label=weeksText, 
						initial=0, 
						required=False
	)
	livedDays = forms.IntegerField(
						label=daysText, 
						initial=0, 
						required=False
	)

	worked = forms.BooleanField(label=_(u"Worked"), required=False)
	workedYears = forms.IntegerField(
						label=yearsText, 
						initial=0, 
						required=False
	)
	workedMonths = forms.IntegerField(
						label=monthsText, 
						initial=0, 
						required=False
	)
	workedWeeks = forms.IntegerField(
						label=weeksText, 
						initial=0, 
						required=False
	)
	workedDays = forms.IntegerField(
						label=daysText, 
						initial=0, 
						required=False
	)

	other = forms.BooleanField(label=_(u"Other"), required=False)
	otherStudyExplanation = forms.CharField(label=_("Please describe"),required=False)
	otherYears = forms.IntegerField(
						label=yearsText, 
						initial=0, 
						required=False
	)
	otherMonths = forms.IntegerField(
						label=monthsText, 
						initial=0, 
						required=False
	)
	otherWeeks = forms.IntegerField(
						label=weeksText, 
						initial=0, 
						required=False
	)
	otherDays = forms.IntegerField(
						label=daysText, 
						initial=0, 
						required=False
	)
	for widg in [school, lived, worked, other]:
		widg.widget.attrs = hideShowAttrs

	for widg in [livedYears, workedYears, otherYears, livedMonths, workedMonths, otherMonths, livedWeeks, workedWeeks, otherWeeks, livedDays, workedDays, otherDays]:
		widg.widget.attrs = timeAttrs

	def __init__(self, *args, **kwargs):
		super(ForeignLangForm, self).__init__(*args, **kwargs)

		self.schoolTotal = 0
		self.livedTotal = 0
		self.workedTotal = 0
		self.otherTotal = 0

		self.needsValidation = True
		self.dayUnits = ["Years", "Months", "Weeks", "Days"]

		self.livedKeys = ["lived" + x for x in self.dayUnits]
		self.workedKeys = ["worked" + x for x in self.dayUnits]
		self.otherKeys = ["other" + x for x in self.dayUnits]
		self.schoolKeys = ["schoolSemesters", "schoolYears"]

		self.errorFieldToKeys = {
			"lived": self.livedKeys,
			"worked": self.workedKeys,
			"other": self.otherKeys,
			"school": self.schoolKeys,
		}

		# adding a hopper for errors so that items
		# aren't immediately removed from cleaned_data
		# Is a list of tuples
		self.errorHopper = []

	def resetHiddenNumInputs(self, cleaned_data):

		# This function will reset values to 0 for conditional
		# inputs that are hidden. For example, if they check
		# "Classes", then inputs for semesters and years appear.
		# If they uncheck classes, we don't want to save values
		# that they had entered to the database, so here we're
		# resetting them to 0.

		for k in self.errorFieldToKeys.keys():
			boolChecked = cleaned_data.get(k)
			if boolChecked == False:
				for t in self.errorFieldToKeys[k]:
					cleaned_data[t] = 0
				if k == "other":
					cleaned_data["otherStudyExplanation"] = u""

		return cleaned_data
		

	def minimumOneStudyContextChecked(self, cleaned_data):

		fieldNames = self.errorFieldToKeys.keys()
		foundChecked = False
		for fn in fieldNames:
			val = cleaned_data.get(fn)
			if val == u"True" or val == True:
				foundChecked = True
				break

		if not foundChecked:
			valError = forms.ValidationError(_("Please check one"), code="required")
			self.errorHopper.append(("school", valError))
			#self.add_error("school", valError)

		return cleaned_data, foundChecked

	def timeRequiredIfContextChecked(self, cleaned_data):

		noErrors = True
		for errorField, keys in self.errorFieldToKeys.iteritems():
			boolChecked = False if errorField not in cleaned_data else cleaned_data[errorField]
			if boolChecked:
				foundValue = False
				for key in keys:
					unitVal = 0 if key not in cleaned_data else cleaned_data[key]
					if unitVal > 0:
						foundValue = True
						break

				if not foundValue:
					noErrors = False
					valError = forms.ValidationError(_("Please tell us how long"), code="blankTime")
					self.errorHopper.append((errorField, valError))
					#self.add_error(errorField, valError)
		return cleaned_data, noErrors

	def calculateTimeTotals(self, cleaned_data):

		semesterKeys = ["schoolSemesters", "schoolYears"]
		valDict = {}
		for k in semesterKeys:
			val = cleaned_data.get(k)
		
			try: 
				val = int(val)
			except ValueError:
				val = 0

			valDict[k] = val

		self.schoolTotal = valDict["schoolSemesters"] + (valDict["schoolYears"] * 2) 

		self.livedTotal = TimeCalculator("lived", cleaned_data).totalDays
		self.workedTotal = TimeCalculator("worked", cleaned_data).totalDays
		self.otherTotal = TimeCalculator("other", cleaned_data).totalDays

		return cleaned_data

	def clean(self):

		cleaned_data = super(ForeignLangForm, self).clean()

		if not self.needsValidation:
			return cleaned_data

		nowRequireds = ["foreignLang", "proficiency"]
		for nowRequired in nowRequireds:
			if not cleaned_data.get(nowRequired):
				valError = forms.ValidationError(FIELD_REQUIRED_MESS, code="required")
				self.errorHopper.append((nowRequired, valError))

		# must check if otherStudyDescription is blank before checking
		# if other has been given a time. This is because if an error
		# is found on an element, it is removed from cleaned_data, if
		# I understand correctly. WAIT: Added an errorHopper to address
		# this. Order should no longer matter
		otherChecked = cleaned_data.get("other")
		if otherChecked == u"True" or otherChecked == True:
			if not cleaned_data.get("otherStudyExplanation"):
				valError = forms.ValidationError(FIELD_REQUIRED_MESS, code="required")
				self.errorHopper.append(("otherStudyExplanation", valError))
				#self.add_error("otherStudyExplanation", valError)

		cleaned_data = self.resetHiddenNumInputs(cleaned_data)

		cleaned_data, oneChecked = self.minimumOneStudyContextChecked(cleaned_data)

		# don't bother checking this if none of them are checked
		if oneChecked:
			cleaned_data, timesGood = self.timeRequiredIfContextChecked(cleaned_data)
			if timesGood:
				cleaned_data = self.calculateTimeTotals(cleaned_data)

		for eTup in self.errorHopper:
			self.add_error(eTup[0], eTup[1])

		self.errorHopper = []

		return cleaned_data



class BaseLangFormSet(BaseFormSet):

	def clean(self):

		#if any(self.errors):
		#	# Don't bother validating the formset if one 
		#	# of the forms has errors
		#	return

		cleaned_data = super(BaseLangFormSet, self).clean()

		# check that two languages aren't the same
		languages = []
		numForms = len(self.forms)
		for i in range(0, numForms):
			form = self.forms[i]
			# Ignore if going to be deleted
			if form.cleaned_data["DELETE"]:
				continue

			lang = form.cleaned_data.get(form.langFieldName)
			if lang in languages:
				raise forms.ValidationError(_("The same language was listed twice"))
			else:
				languages.append(lang)
				
class TimeCalculator(object):

	def __init__(self, prefix, cleaned_data):

		units = ["Years", "Months", "Weeks", "Days"]
		keys = [prefix + x for x in units]

		vals =[] 
		for k in keys:
			val = cleaned_data.get(k)
		
			try: 
				val = int(val)
			except(ValueError, TypeError) as e:
				val = 0

			vals.append(val)

		years = vals[0]
		months = vals[1]
		weeks = vals[2]
		days = vals[3]
		self.totalDays = (years * 365) + (months * 30) + (weeks * 7) + days
