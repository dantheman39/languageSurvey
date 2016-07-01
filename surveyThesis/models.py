from django.db import models

from surveyThesis.constants import ED_CHOICES, UG_CHOICES, LANGUAGE_CHOICES, YES_NO_CHOICES

class SurveyLine(models.Model):

	print("Make this unique")
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

	visionProblems = models.BooleanField(choices=YES_NO_CHOICES)
	visionProblemsDetails = models.TextField(blank=True)

	readingProblems = models.BooleanField(choices=YES_NO_CHOICES)
	readingProblemsDetails = models.TextField(blank=True)

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

	proficiency = models.IntegerField(blank=True)

	school = models.BooleanField(default=False)
	schoolSemesters = models.IntegerField(null=True, blank=True)
	livedAbroad = models.BooleanField(default=False)
	livedAbroadDays = models.IntegerField(null=True, blank=True)
	other = models.BooeanField(default=False)
	otherDescription = models.CharField(max_length=255, blank=True)
	otherDays = models.IntegerField(null=True, blank=True)
