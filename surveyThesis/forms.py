#!/usr/bin/env python
#-*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext as _

class PageOne(forms.Form):
	defErrMess = _(u'This field is required')
	age = forms.IntegerField(label=_(u'Age'),
				label_suffix='',
				error_messages={'required': defErrMess},
				localize=True,
				)
	education = forms.ChoiceField(label=_(u'Education level'),
				label_suffix='',
				error_messages={'required': defErrMess},
				localize=True,
				choices=(_(u'None'), _(u'Secondary'), _(u'Secondary')),
				)
