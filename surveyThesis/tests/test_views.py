#!/usr/bin/env python3
#-*- coding: UTF-8 -*-

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from surveyThesis.models import SurveyLine, NativeLangLine, HeritageLangLine, ForeignLangLine
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

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

	def test_new_user_correct_template(self):

		login = self.loginUser(user_num=1)
		response = self.client.get(reverse("survey"))
		self.assertTemplateUsed(response, "survey.html")

	def test_already_submitted_correct_template(self):

		login = self.loginUser(user_num=2)
		response = self.client.get(reverse("survey"))
		self.assertTemplateUsed(response, "alreadySubmitted.html")

	def test_delete(self):

		# Deleting testuser2's entries, keep this at
		# the bottom of file for now

		login = self.loginAdmin()

		response = self.client.post(reverse("delete", args=[1]))

		self.assertEqual(response.status_code, 200)

		with self.assertRaises(ObjectDoesNotExist) as e:
			SurveyLine.objects.get(pk=1)

		with self.assertRaises(ObjectDoesNotExist) as e:
			NativeLangLine.objects.get(surveyId=1)

		with self.assertRaises(ObjectDoesNotExist) as e:
			HeritageLangLine.objects.get(surveyId=1)

		with self.assertRaises(ObjectDoesNotExist) as e:
			ForeignLangLine.objects.get(surveyId=1)
