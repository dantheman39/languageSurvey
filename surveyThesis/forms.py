#!/usr/bin/env python
#-*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext as _
from surveyThesis.models import SurveyLine

#class PageOne(forms.Form):
#	defErrMess = _(u'This field is required')
#	age = forms.IntegerField(label=_(u'Age'),
#				label_suffix='',
#				error_messages={'required': defErrMess},
#				localize=True,
#				)
#	education = forms.ChoiceField(label=_(u'Education level'),
#				label_suffix='',
#				error_messages={'required': defErrMess},
#				localize=True,
#				choices=(_(u'None'), _(u'Secondary'), _(u'Secondary')),
#				)

class PageOne(ModelForm):

	class Meta:
		model = SurveyLine
		fields = [
				'participantNumber', 
				'age', 
				'education', 
				'undergradLevel',
				'nativeLanguage',
				]
		#localized_fields = fields

		labels = {
			'participantNumber': _(u"Participant number"),
			'age': _(u"Age"),
			'education': _(u"Education"),
			'nativeLanguage': _(u"Native language"),
		}
