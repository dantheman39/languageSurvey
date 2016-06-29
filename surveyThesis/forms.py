#!/usr/bin/env python
#-*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext as _
from surveyThesis.models import SurveyLine, ForeignLangLine
from surveyThesis.constants import ED_CHOICES, LANGUAGE_CHOICES, UG_CHOICES, FIELD_REQUIRED_MESS
import logging

logger = logging.getLogger('surveyThesis')

class PageOne(forms.Form):

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
				required=True,
				)

	nativeLanguages = forms.CharField(
				max_length=200,
				)

	nativeLanguageLabel = _(u"native language")
	addLanguageButtonText = _(u"add language")
	removeButtonText = _(u"remove")
	fieldRequiredMess = _(u"this field is required")
	visionDifficultiesText = _(u"do you have any vision or hearing problems? if yes and you are comfortable doing so, please explain.")
	readingDifficultiesText = _(u"do you have any difficulty reading? if yes and you are comfortable doing so, please explain.")
	undergradBlankError = _(u"Please tell us what year you are in, or the last year you completed")

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
