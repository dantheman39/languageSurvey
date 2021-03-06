#!/usr/bin/env python3
#-*- coding: UTF-8 -*-

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from surveyThesis.models import SurveyLine, NativeLangLine, HeritageLangLine, ForeignLangLine
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from surveyThesis.forms import FIELD_REQUIRED_MESS

class ViewTests(TestCase):

	fixtures = ["testusers.json"]
	### Note that testuser1 has no submission, testuser2 does

	@classmethod
	def setUpTestData(self):
		test_user1 = User.objects.create_user(username="testuser1", password="12345")
		test_admin1 = User.objects.create_user(username="testadmin1", 
										password="12345", is_staff=True)
		test_user1.save()
		test_admin1.save()

		# This user will have test data
		test_user2 = User.objects.create_user(username="testuser2", password="12345")
		test_user2.save()

	def loginUser(self, user_num):

		user = "testuser" + unicode(user_num)

		return self.client.login(username=user, password="12345")

	def loginAdmin(self):

		return self.client.login(username="testadmin1", password="12345")

	# For view method surveyPage
	def test_survey_new_user_correct_template(self):

		login = self.loginUser(user_num=1)
		response = self.client.get(reverse("survey"))
		self.assertTemplateUsed(response, "survey.html")

	# For view method surveyPage
	def test_survey_already_submitted_correct_template(self):

		login = self.loginUser(user_num=2)
		response = self.client.get(reverse("survey"))
		self.assertTemplateUsed(response, "alreadySubmitted.html")

	def test_results_correct_template(self):

		login = self.loginAdmin()
		response = self.client.get(reverse("results"))
		self.assertTemplateUsed(response, "results.html")

	def test_delete(self):

		# Deleting testuser2's entries, keep this at
		# the bottom of file for now

		login = self.loginAdmin()

		response = self.client.post(reverse("delete", args=[1]))

		self.assertEqual(response.status_code, 200)

		# Making sure object and related tables don't exist
		with self.assertRaises(ObjectDoesNotExist) as e:
			SurveyLine.objects.get(pk=1)

		with self.assertRaises(ObjectDoesNotExist) as e:
			NativeLangLine.objects.get(surveyId=1)

		with self.assertRaises(ObjectDoesNotExist) as e:
			HeritageLangLine.objects.get(surveyId=1)

		with self.assertRaises(ObjectDoesNotExist) as e:
			ForeignLangLine.objects.get(surveyId=1)

	### Higher level (integration) tests
	def test_survey_valid_post(self):

		login = self.loginUser(user_num=1)
		postData = {
			"natLang-INITIAL_FORMS": 0,
			"natLang-TOTAL_FORMS": 1,
			"natLang-MIN_NUM_FORMS": 1,
			"natLang-MAX_NUM_FORMS": 1000,
			"natLang-0-nativeLang": "en",
			"forLang-INITIAL_FORMS": 0,
			"forLang-TOTAL_FORMS": 2,
			"forLang-MIN_NUM_FORMS": 0,
			"forLang-MAX_NUM_FORMS": 1000,
			"herLang-INITIAL_FORMS": 0,
			"herLang-TOTAL_FORMS": 2,
			"herLang-MIN_NUM_FORMS": 0,
			"herLang-MAX_NUM_FORMS": 1000,
			"visionProblems": False,
			"hearingProblems": False,
			"education": "primary",
			"heritageLangBool": False,
			"foreignLangBool": False,
			"gender": "male",
			"age": 21,

		}
		response = self.client.post(reverse("survey"), postData) 
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "completed.html")

	def test_survey_bad_post(self):

		login = self.loginUser(user_num=1)
		#"age" is missing
		postData = {
			"natLang-INITIAL_FORMS": 0,
			"natLang-TOTAL_FORMS": 1,
			"natLang-MIN_NUM_FORMS": 1,
			"natLang-MAX_NUM_FORMS": 1000,
			"natLang-0-nativeLang": "en",
			"forLang-INITIAL_FORMS": 0,
			"forLang-TOTAL_FORMS": 2,
			"forLang-MIN_NUM_FORMS": 0,
			"forLang-MAX_NUM_FORMS": 1000,
			"herLang-INITIAL_FORMS": 0,
			"herLang-TOTAL_FORMS": 2,
			"herLang-MIN_NUM_FORMS": 0,
			"herLang-MAX_NUM_FORMS": 1000,
			"visionProblems": True,
			"hearingProblems": False,
			"education": "primary",
			"heritageLangBool": False,
			"foreignLangBool": False,
			"gender": "male",

		}
		response = self.client.post(reverse("survey"), postData)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "survey.html")
		self.assertFormError(response, "form", "age", FIELD_REQUIRED_MESS)

	def test_survey_valid_edit(self):

		login = self.loginAdmin()
		postData = {
			"natLang-INITIAL_FORMS": 0,
			"natLang-TOTAL_FORMS": 1,
			"natLang-MIN_NUM_FORMS": 1,
			"natLang-MAX_NUM_FORMS": 1000,
			"natLang-0-nativeLang": "en",
			"forLang-INITIAL_FORMS": 0,
			"forLang-TOTAL_FORMS": 2,
			"forLang-MIN_NUM_FORMS": 0,
			"forLang-MAX_NUM_FORMS": 1000,
			"herLang-INITIAL_FORMS": 0,
			"herLang-TOTAL_FORMS": 2,
			"herLang-MIN_NUM_FORMS": 0,
			"herLang-MAX_NUM_FORMS": 1000,
			"visionProblems": False,
			"hearingProblems": False,
			"education": "primary",
			"heritageLangBool": False,
			"foreignLangBool": False,
			"gender": "male",
			"age": 21,

		}
		response = self.client.post(reverse("viewOne", args=[1]), postData) 
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "editSuccessful.html")
