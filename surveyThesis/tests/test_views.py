#!/usr/bin/env python3
#-*- coding: UTF-8 -*-

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from surveyThesis.models import SurveyLine, NativeLangLine, HeritageLangLine, ForeignLangLine
from django.utils import timezone

class ViewTests(TestCase):

	def setUp(self):
		test_user1 = User.objects.create_user(username="testuser1", password="12345")
		test_admin1 = User.objects.create_user(username="testadmin1", 
										password="12345", is_staff=True)
		test_user1.save()
		test_admin1.save()

		# This user will have test data
		test_user2 = User.objects.create_user(username="testuser2", password="12345")
		test_user2.save()

		survey_line = SurveyLine(
			userName=test_user2.username,
			age=19,
			gender="male",
			education="undergrad",
			undergradLevel="sp",
			date=timezone.now(),
			dateLastEdited=timezone.now(),
			visionProblems=True,
			visionProblemsDetails="I have ants in my eyes",
			hearingProblems=True,
			hearingProblemsDetails="I'm deaf",
			foreignLangBool=True,
			heritageLangBool=True,
		)
		survey_line.save()

		native_lang = NativeLangLine(
			surveyId=survey_line,
			nativeLang="en",
		)
		native_lang.save()

		heritage_lang = HeritageLangLine(
			surveyId=survey_line,
			heritageLang="es",
			explanation="Spoke Spanish with my mom",
		)	
		heritage_lang.save()

		foreign_lang = ForeignLangLine(
			surveyId=survey_line,
			foreignLang="fr",
			proficiency=2,
			school=True,
			schoolSemestersTotal=8,
			schoolSemesters=0,
			schoolYears=4,
			other=True,
			otherDescription="I watch movies",
			otherDaysTotal=365,
			otherYears=1,
			otherMonths=0,
			otherWeeks=0,
			otherDays=0,
		)
		foreign_lang.save()
		

	def loginUser(self, user_num=1):

		user = "testuser" + unicode(user_num)

		return self.client.login(username=user, password="12345")

	def loginAdmin(self):

		return self.client.login(username="testadmin1", password="12345")

	def test_new_user_correct_template(self):

		login = self.loginUser()
		response = self.client.get(reverse("survey"))
		self.assertTemplateUsed(response, "survey.html")

	def test_old_user_redirected(self):

		login = self.loginUser(user_num=2)
		response = self.client.get(reverse("survey"))
		self.assertTemplateUsed(response, "alreadySubmitted.html")
