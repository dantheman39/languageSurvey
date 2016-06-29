#!/usr/bin/env python
#-*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext as _
from surveyThesis.models import SurveyLine, ForeignLangLine
from surveyThesis.constants import ED_CHOICES, UG_CHOICES, LANGUAGE_CHOICES, YES_NO_CHOICES
import logging

logger = logging.getLogger('surveyThesis')

class PageOne(forms.Form):

	nativeLanguageLabel = _(u"Native language")

	addLanguageButtonText = _(u"Add language")
	removeButtonText = _(u"Remove")

	fieldRequiredMess = _(u"This field is required")

	visionProblemsText = _(u"Do you have any vision or hearing problems?")
	visionProblemsDetailsText = _(u"If you are comfortable doing so, please explain.")

	readingProblemsText = _(u"Do you have any difficulty reading?")
	readingProblemsDetailsText = visionProblemsDetailsText

	undergradBlankError = _(u"Please tell us what year you are in, or the last year you completed")

	foreignLangsQuestion = _(u"Do you speak, or have you studied a foreign language?")
	foreignLangLabel = _(u"Which one?")
	
	methodOfStudyQuestion = _(u"How did you learn or use it? (Check all that apply)")
	
	semestersQuestion = _(u"About how many semesters did you study for? (one semester is about 5 months, one year is two semesters) ")
	semestersText = _(u"Semesters")
	years = _(u"Years")

	livedQuestion = _(u"About how long were you there?")
	yearsText = _(u"Years")
	monthsText = _(u"Months")
	weeksText = _(u"Weeks")
	daysText = _(u"Days")

	otherForeignDetails = _(u"Please explain")

	# need this so that I can send it to the form
	languageChoices = LANGUAGE_CHOICES

	participantNumber = forms.IntegerField(label=_(u'Participant number'),
				label_suffix='',
				error_messages={'required': fieldRequiredMess},
				)
	age = forms.IntegerField(label=_(u'Age'),
				label_suffix='',
				error_messages={'required': fieldRequiredMess},
				#localize=True,
				)
	education = forms.ChoiceField(label=_(u'Education level'),
				label_suffix='',
				error_messages={'required': fieldRequiredMess},
				choices=ED_CHOICES,
				)

	undergradLevel = forms.ChoiceField(label=_(u'Undergrad level'),
				label_suffix='',
				error_messages={'required': fieldRequiredMess},
				choices=UG_CHOICES,
				required=True,
				)

	nativeLanguages = forms.CharField(
				max_length=200,
				)

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

	foreignLanguages = forms.TextField()

	def clean(self):
		cleaned_data = super(PageOne, self).clean()

		try:
			educationSelection = cleaned_data['education']
			if cleaned_data['education'] == "undergrad":
				if not cleaned_data['undergradLevel']:
					valError = forms.ValidationError(self.undergradBlankError)
					self.add_error('undergradLevel', valError)

		# means didn't pass cleaning
		except KeyError:
			pass

		# check foreign language logic

		return cleaned_data

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
