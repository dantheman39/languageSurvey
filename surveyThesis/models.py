from django.db import models

from surveyThesis.constants import ED_CHOICES, UG_CHOICES, LANGUAGE_CHOICES, YES_NO_CHOICES, GENDER_CHOICES

class SurveyLine(models.Model):

	userName = models.CharField(unique=True, max_length=50)
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

	date = models.DateTimeField()
	dateLastEdited = models.DateTimeField(auto_now=True)

	visionProblems = models.BooleanField(choices=YES_NO_CHOICES)
	visionProblemsDetails = models.TextField(blank=True)

	hearingProblems = models.BooleanField(choices=YES_NO_CHOICES)
	hearingProblemsDetails = models.TextField(blank=True)

	foreignLangBool = models.BooleanField(choices=YES_NO_CHOICES)
	heritageLangBool = models.BooleanField(choices=YES_NO_CHOICES)

	adminComment = models.TextField(blank=True)

class NativeLangLine(models.Model):

	surveyId = models.ForeignKey('SurveyLine')

	nativeLang = models.CharField(
		max_length=10,
	)

class HeritageLangLine(models.Model):

	surveyId = models.ForeignKey('SurveyLine')

	heritageLang = models.CharField(
		max_length=10,
	)

	explanation = models.CharField(max_length=255, blank=True)

class ForeignLangLine(models.Model):

	surveyId = models.ForeignKey('SurveyLine')
	
	foreignLang = models.CharField(
		max_length=10,
	)

	proficiency = models.IntegerField()

	school = models.BooleanField(default=False)
	schoolSemestersTotal = models.IntegerField(default=0)
	schoolYears = models.IntegerField(default=0)
	schoolSemesters = models.IntegerField(default=0)

	lived= models.BooleanField(default=False)
	livedDaysTotal = models.IntegerField(default=0)
	livedYears = models.IntegerField(default=0)
	livedMonths = models.IntegerField(default=0)
	livedWeeks = models.IntegerField(default=0)
	livedDays = models.IntegerField(default=0)

	worked = models.BooleanField(default=False)
	workedDaysTotal = models.IntegerField(default=0)
	workedYears = models.IntegerField(default=0)
	workedMonths = models.IntegerField(default=0)
	workedWeeks = models.IntegerField(default=0)
	workedDays = models.IntegerField(default=0)

	other = models.BooleanField(default=False)
	otherDescription = models.CharField(max_length=255, blank=True)
	otherDaysTotal = models.IntegerField(default=0)
	otherYears = models.IntegerField(default=0)
	otherMonths = models.IntegerField(default=0)
	otherWeeks = models.IntegerField(default=0)
	otherDays = models.IntegerField(default=0)

