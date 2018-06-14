#!/usr/bin/env python
#-*- coding: utf-8 -*-

from django.test import TestCase
from surveyThesis.forms import PageOne, NativeLangForm, HeritageLangForm, ForeignLangForm, BaseLangFormSet, TimeCalculator, FIELD_REQUIRED_MESS, SORTOF_OPTIONAL

class FormTests(TestCase):

	## Have tests for NativeLangForm and HeritageLangForm, write more for the rest

	def test_native_lang_blank(self):

		natLangForm = NativeLangForm(data={})
		self.assertFalse(natLangForm.is_valid())
		self.assertEqual(natLangForm.errors, {
			"nativeLang": [FIELD_REQUIRED_MESS]
		})

	def test_native_lang_valid_data(self):

		natLangForm = NativeLangForm(data={"nativeLang": "en"})

		self.assertTrue(natLangForm.is_valid())
		self.assertEqual(natLangForm.cleaned_data["nativeLang"], "en")

	def test_heritage_lang_blank_now_required(self):

		herLangForm = HeritageLangForm(data={})
		self.assertFalse(herLangForm.is_valid())
		self.assertEqual(herLangForm.errors, {
			"heritageLang": [FIELD_REQUIRED_MESS],
			"explanation": [SORTOF_OPTIONAL],
		})

	# The HeritageLangForm is only required if PageOne.heritageLangBool is 
	# True (will have to check this in integration tests). But to make
	# that happen, HeritageLangForm has a .needsValidation attritbute,
	# which is set to False in views.py if heritageLangBool == False.
	# Not pretty, but I couldn't find a better way to do it.
	def test_heritage_lang_blank_ok(self):

		herLangForm = HeritageLangForm(data={})
		herLangForm.needsValidation = False
		self.assertTrue(herLangForm.is_valid())

	def test_heritage_lang_all_fields_valid(self):

		herLangForm = HeritageLangForm(data={
			"heritageLang": "es",
			"explanation": "My mom talked to me",
		})
		self.assertTrue(herLangForm.is_valid())
		self.assertTrue(herLangForm.cleaned_data["heritageLang"] == "es")
		self.assertTrue(herLangForm.cleaned_data["explanation"] == "My mom talked to me")
