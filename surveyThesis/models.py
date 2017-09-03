from django.db import models

from surveyThesis.constants import ED_CHOICES, UG_CHOICES, LANGUAGE_CHOICES, YES_NO_CHOICES, GENDER_CHOICES

class SurveyLine(models.Model):

	print("Make this unique")
	participantNumber = models.IntegerField()
	age = models.IntegerField()
	gender = models.CharField(
		choices=GENDER_CHOICES,
		max_length=50,
	)

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

	visionProblems = models.BooleanField(choices=YES_NO_CHOICES)
	visionProblemsDetails = models.TextField(blank=True)

	hearingProblems = models.BooleanField(choices=YES_NO_CHOICES)
	hearingProblemsDetails = models.TextField(blank=True)

	foreignLangBool = models.BooleanField(choices=YES_NO_CHOICES)

class NativeLangLine(models.Model):

	surveyId = models.ForeignKey('SurveyLine')

	nativeLang = models.CharField(
		max_length=10,
	)

class ForeignLangLine(models.Model):

	surveyId = models.ForeignKey('SurveyLine')
	
	foreignLang = models.CharField(
		max_length=10,
	)

	proficiency = models.IntegerField()

	school = models.BooleanField(default=False)
	schoolSemesters = models.IntegerField(default=0)
	livedAbroad = models.BooleanField(default=False)
	livedAbroadDays = models.IntegerField(default=0)
	worked = models.BooleanField(default=False)
	workedDays = models.IntegerField(default=0)
	other = models.BooleanField(default=False)
	otherDescription = models.CharField(max_length=255, blank=True)
	otherDays = models.IntegerField(default=0)
