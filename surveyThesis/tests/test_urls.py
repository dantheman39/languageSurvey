#!/usr/bin/env python3
#-*- coding: UTF-8 -*-

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

# Just beginning to work with real unit tests.
class UrlTests(TestCase):

	fixtures = ["testusers.json"]

	@classmethod
	def setUpTestData(self):
		test_user1 = User.objects.create_user(username="testuser1", password="12345")
		test_admin1 = User.objects.create_user(username="testadmin1", 
										password="12345", is_staff=True)
		test_user1.save()
		test_admin1.save()

	def test_logged_in(self):
		login = self.client.login(username="testuser1", password="12345")
		response = self.client.get(reverse("survey"))

		# check that user is logged in
		self.assertEqual(unicode(response.context["user"]), u"testuser1")
		# check that we got a success response
		self.assertEqual(response.status_code, 200)

	def test_redirect_if_not_logged_in(self):
		response = self.client.get(reverse("survey"))
		self.assertRedirects(response, "/accounts/login/?next=/")

	def test_redirect_if_not_admin(self):
		login = self.client.login(username="testuser1", password="12345")
		response = self.client.get(reverse("results"))
		self.assertRedirects(response, "/admin/login/?next=/results/")

	def test_results_view_one_with_arg(self):

		login = self.client.login(username="testadmin1", password="12345")
		response = self.client.get(reverse("viewOne", args=[1]))
		self.assertEqual(response.status_code, 200)
