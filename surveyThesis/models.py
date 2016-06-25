from django.db import models

from django.utils.translation import ugettext as _
from surveyThesis.constants import *

class SurveyLine(models.Model):

	participantNumber = models.IntegerField()
	age = models.IntegerField()

	education = models.CharField(
		choices=ED_CHOICES,
		max_length=50,
	)

	undergradLevel = models.CharField(
		choices=UG_CHOICES,
		max_length=50,
		blank=True,
	)
	date = models.DateTimeField(auto_now=True)
	
	nativeLanguage1 = models.CharField(
		choices=LANGUAGE_CHOICES,
		max_length=50,
	)

	nativeLanguage2 = models.CharField(
		choices=LANGUAGE_CHOICES,
		max_length=50,
		blank=True,
	)

	nativeLanguage3 = models.CharField(
		choices=LANGUAGE_CHOICES,
		max_length=50,
		blank=True,
	)
	
	nativeLanguage4 = models.CharField(
		choices=LANGUAGE_CHOICES,
		max_length=50,
		blank=True,
	)
