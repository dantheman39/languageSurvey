#!/usr/bin/env python
#-*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext as _
from surveyThesis.models import SurveyLine, ForeignLangLine
from surveyThesis.constants import ED_CHOICES, UG_CHOICES, LANGUAGE_CHOICES, YES_NO_CHOICES, PROFICIENCY_CHOICES
import logging

logger = logging.getLogger('surveyThesis')
FIELD_REQUIRED_MESS = _(u"This field is required")

class PageOne(forms.Form):

	pageTitle = _(u"Language background survey")

	nativeLanguageLabel = _(u"Native language")
	nativeLangLegend = _(u"Native language(s)")

	addLanguageButtonText = _(u"+")
	removeButtonText = _(u"-")

	visionProblemsText = _(u"Do you have any vision or hearing problems?")
	visionProblemsDetailsText = _(u"If you are comfortable doing so, please explain.")

	readingProblemsText = _(u"Do you have any difficulty reading?")
	readingProblemsDetailsText = visionProblemsDetailsText

	undergradBlankError = _(u"Please tell us what year you are in, or the last year you completed")

	foreignLangsQuestion = _(u"Do you speak, or have you studied a foreign language?")

	# need this so that I can send it to the form
	languageChoices = LANGUAGE_CHOICES

	participantNumber = forms.IntegerField(label=_(u'Participant number'),
				label_suffix='',
				error_messages={'required': FIELD_REQUIRED_MESS},
				)
	age = forms.IntegerField(label=_(u'Age'),
				label_suffix='',
				error_messages={'required': FIELD_REQUIRED_MESS},
				#localize=True,
				)
	education = forms.ChoiceField(label=_(u'Education level'),
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
				)

	readingProblems = forms.ChoiceField(
				choices=YES_NO_CHOICES,
				widget=forms.RadioSelect,
				)

	readingProblemsDetails = forms.CharField(
				required=False,
				widget = forms.Textarea,
				)

	#foreignLanguages = forms.CharField(
	#			widget = forms.Textarea,
	#			)

	foreignLangBool = forms.ChoiceField(
				choices=YES_NO_CHOICES,
				widget=forms.RadioSelect,
				)

	foreignProficiencyChoices = PROFICIENCY_CHOICES 


	def clean(self):
		cleaned_data = super(PageOne, self).clean()

		if 'education' in cleaned_data:
			educationSelection = cleaned_data['education']
			if cleaned_data['education'] == "undergrad":
				if 'undergradLevel' not in cleaned_data or not cleaned_data['undergradLevel']:
					valError = forms.ValidationError(self.undergradBlankError)
					self.add_error('undergradLevel', valError)

		# check foreign language logic

		return cleaned_data

class NativeLangForm(forms.Form):

	nativeLang = forms.ChoiceField(label=_(u'Native language'),
				label_suffix='',
				error_messages={'required': FIELD_REQUIRED_MESS},
				choices=LANGUAGE_CHOICES,
				)

class ForeignLangForm(forms.Form):

	foreignLangLabel = _(u"Which one?")
	foreignLang = forms.ChoiceField(
					label=foreignLangLabel,
					label_suffix='',
					error_messages={'required': FIELD_REQUIRED_MESS},
					choices=LANGUAGE_CHOICES,
				)

	foreignProfLabel = _(u"Estimated proficiency")
	proficiency = forms.ChoiceField(
					label=foreignProfLabel,
					label_suffix='',
					error_messages={'required': FIELD_REQUIRED_MESS},
					choices=PROFICIENCY_CHOICES,
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

	school = forms.BooleanField(label=_(u"Classes"))
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

	lived = forms.BooleanField(label=_(u"Lived"))
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

	worked = forms.BooleanField(label=_(u"Worked"))
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

	other = forms.BooleanField(label=_(u"Other"))
	otherStudyExplanation = forms.CharField(label=_("What was it?"),required=False)
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


#class PageOne(ModelForm):
#
#	class Meta:
#		model = SurveyLine
#		fields = [
#				'participantNumber', 
#				'age', 
#				'education', 
#				'undergradLevel',
#				'nativeLanguage1',
#				'nativeLanguage2',
#				'nativeLanguage3',
#				'nativeLanguage4',
#				]
#		#localized_fields = fields
#
#		labels = {
#			'participantNumber': _(u"Participant number"),
#			'age': _(u"Age"),
#			'education': _(u"Education"),
#			'undergradLevel': _(u"Undergrad level"),
#			'nativeLanguage1': _(u"Native language"),
#			'nativeLanguage2': _(u"Native language"),
#			'nativeLanguage3': _(u"Native language"),
#			'nativeLanguage4': _(u"Native language"),
#		}
#
#	def clean(self):
#		cleaned_data = super(PageOne, self).clean()
#
#		try:
#			educationSelection = cleaned_data['education']
#			if cleaned_data['education'] == "undergrad":
#				if not cleaned_data['undergradLevel']:
#					valError = forms.ValidationError(_(u"Please tell us what year you are in, or the last year you completed"))
#					self.add_error('undergradLevel', valError)
#
#		# means didn't pass cleaning
#		except KeyError:
#			pass
#
#		return cleaned_data
