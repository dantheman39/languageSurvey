#!/usr/bin/env python
#-*- coding: utf-8 -*-

from django.test import TestCase
from surveyThesis.forms import SurveyForm, NativeLangForm, HeritageLangForm, ForeignLangForm, BaseLangFormSet, FIELD_REQUIRED_MESS, SORTOF_OPTIONAL, STUDY_TIME_MESS, DUPLICATE_LANG_MESS
from django.forms import formset_factory

class FormTests(TestCase):

	#### NativeLangForm

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

	#### HeritageLangForm

	# The HeritageLangForm is only required if SurveyForm.heritageLangBool is 
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

	#### SurveyForm
	def test_survey_blank(self):

		survey = SurveyForm(data={})
		self.assertFalse(survey.is_valid())
		
		requireds = [
			"age",
			"gender",
			"education",
			"visionProblems",
			"hearingProblems",
			"heritageLangBool",
			"foreignLangBool",
		]

		notPresent = "The required field \"{}\" did not appear in the list of errors, or the error messageit generated was not correct"
		requiredMess = "The custom FIELD_REQUIRED_MESS was not used as the error message for field \"{}\""
		for required in requireds:

			self.assertTrue(survey.has_error(required), msg=notPresent.format(required))

			self.assertTrue(survey.errors[required] == [FIELD_REQUIRED_MESS], 
							msg=requiredMess.format(required)) 

		# Make sure there are no errors in the list beyond the ones we're expecting
		for error, msg in survey.errors.iteritems():
			self.assertTrue(error in requireds, msg="An additional error was found, \"{}\" but is unaccounted for by the test.".format(error))

	def test_survey_valid(self):

		# Not including optional fields, will be tested in different test
		data = {
			"adminComment": "Admin comment",
			"age": 12,
			"gender": "male",
			"education": "primary",
			"visionProblems": False, 
			"hearingProblems": False,
			"heritageLangBool": False,
			"foreignLangBool": False,
		}

		survey = SurveyForm(data=data)
		self.assertTrue(survey.is_valid())

	def test_survey_undergrad_now_required(self):

		# If education == undergrad, undergradLevel can't be blank
		data = {
			"adminComment": "Admin comment",
			"age": 12,
			"gender": "male",
			"education": "undergrad",
			"visionProblems": False, 
			"hearingProblems": False,
			"heritageLangBool": False,
			"foreignLangBool": False,
		}

		survey = SurveyForm(data=data)
		self.assertFalse(survey.is_valid())
		# Make sure the error message is correct
		self.assertEqual(survey.errors["undergradLevel"], [survey.undergradBlankError])

		# Submit a good form
		data["undergradLevel"] = "fr"
		survey = SurveyForm(data=data)
		self.assertTrue(survey.is_valid())

	def test_survey_vision_hearing_now_required(self):
	
		# If hearingProblems == True or visionProblems == True, 
		# hearingProblemsDetails and/or visionProblemsDetails are now required
		data = {
			"adminComment": "Admin comment",
			"age": 12,
			"gender": "male",
			"education": "primary",
			"visionProblems": True, 
			"hearingProblems": True,
			"heritageLangBool": False,
			"foreignLangBool": False,
		}
		survey = SurveyForm(data=data)

		self.assertFalse(survey.is_valid())

		self.assertEqual(survey.errors, {
			"hearingProblemsDetails": [SORTOF_OPTIONAL],
			"visionProblemsDetails": [SORTOF_OPTIONAL],
		})

	def test_survey_castBooleanText(self):

		survey = SurveyForm(data={
			"visionProblems": "True",
			"hearingProblems": "False",
		})
		survey.is_valid()
		self.assertEqual(type(survey.cleaned_data["visionProblems"]), bool)
		self.assertEqual(type(survey.cleaned_data["hearingProblems"]), bool)
		self.assertEqual(survey.cleaned_data["visionProblems"], True)
		self.assertEqual(survey.cleaned_data["hearingProblems"], False)

	#### ForeignLangForm
	def test_foreign_blank(self):

		fl = ForeignLangForm(data={})
		self.assertFalse(fl.is_valid())
		
		requireds = [
			"foreignLang",
			"proficiency",
		]

		notPresent = "The required field \"{}\" did not appear in the list of errors, or the error messageit generated was not correct"
		requiredMess = "The custom FIELD_REQUIRED_MESS was not used as the error message for field \"{}\""
		for required in requireds:

			self.assertTrue(fl.has_error(required), msg=notPresent.format(required))

			self.assertTrue(fl.errors[required] == [FIELD_REQUIRED_MESS], 
							msg=requiredMess.format(required)) 

		# making sure "school" shows an error. This is the field associated with
		# the error for when no single study context has been checked
		self.assertTrue(fl.has_error("school"), msg="The \"school\" error was not present")

		allErrors = [r for r in requireds]
		allErrors.append("school")

		# Make sure there are no errors in the list beyond the ones we're expecting
		for error, msg in fl.errors.iteritems():
			self.assertTrue(error in allErrors, msg="An additional error was found, \"{}\" but is unaccounted for by the test.".format(error))

	# See the message for test_heritage_lang_blank_ok
	def test_foreign_blank_ok(self):

		fl = ForeignLangForm(data={})
		fl.needsValidation = False
		self.assertTrue(fl.is_valid())


	def test_foreign_valid(self):

		data = {
			"foreignLang": "es",
			"proficiency": 1,
			"school": True,
			"schoolSemesters": 1,
			"schoolYears": 1,
			"lived": True,
			"livedYears": 1,
			"livedMonths": 1,
			"livedWeeks": 1,
			"livedDays": 1,
			"worked": True,
			"workedYears": 1,
			"workedMonths": 1,
			"workedWeeks": 1,
			"workedDays": 1,
			"other": True,
			"otherStudyExplanation": "Books",
			"otherYears": 1,
			"otherMonths": 1,
			"otherWeeks": 1,
			"otherDays": 1,
		}
		fl = ForeignLangForm(data=data)
		self.assertTrue(fl.is_valid())

	def test_foreign_study_time_now_required(self):

		data = {
			"foreignLang": "es",
			"proficiency": 1,
			"school": True,
			"schoolSemesters": 1,
			"schoolYears": 1,
			"lived": True,
			"worked": True,
			"other": True,
		}

		studyTimeErrors = [
			"lived",
			"worked",
			"other",
		]

		fl = ForeignLangForm(data=data)
		self.assertFalse(fl.is_valid())

		allErrors = [x for x in studyTimeErrors]
		allErrors.append("otherStudyExplanation")
		
		for error in allErrors:
			self.assertTrue(error in allErrors, 
				msg="\"{}\" not found in errors".format(error))

		# Make sure error message is correct
		for studyTime in studyTimeErrors:
			self.assertEqual(fl.errors[studyTime], [STUDY_TIME_MESS])

		self.assertEqual(fl.errors["otherStudyExplanation"], [FIELD_REQUIRED_MESS])

		# Make sure we got all errors
		for error in fl.errors:
			self.assertTrue(error in allErrors, 
							msg="The error \"{}\" was not tested.".format(error))

	def test_study_time(self):

		cleaned_data = {
			"lived": True,
			"livedYears": 1,
			"livedMonths": 1,
			"livedWeeks": 1,
			"livedDays": 1,
			"worked": True,
			"workedYears": 1,
			"workedMonths": 1,
			"workedWeeks": 1,
			"workedDays": 1,
			"other": True,
			"otherYears": 1,
			"otherMonths": 1,
			"otherWeeks": 1,
			"otherDays": 1,
			"school": True,
			"schoolSemesters": 1,
			"schoolYears": 1,
		}

		fl = ForeignLangForm(data=cleaned_data)

		# Test the day function directly
		lived = fl.calculateStudyDays("lived", cleaned_data)
		worked = fl.calculateStudyDays("worked", cleaned_data)
		other = fl.calculateStudyDays("other", cleaned_data)
		for t in [lived, worked, other]:
			self.assertEqual(t, 403)

		fl.is_valid()
		self.assertEqual(fl.livedTotal, 403)
		self.assertEqual(fl.workedTotal, 403)
		self.assertEqual(fl.otherTotal, 403)
		# Semesters
		self.assertEqual(fl.schoolTotal, 3)


	### BaseLangFormSet
	def test_BaseLangFormSet_valid(self):

		NatLangFormset = formset_factory(
							NativeLangForm, 
							min_num=1,
							validate_min=True, 
							extra=0,
							can_delete=True,
							formset=BaseLangFormSet,
		)

		postData = {
			"natLang-INITIAL_FORMS": 0,
			"natLang-TOTAL_FORMS": 2,
			"natLang-MIN_NUM_FORMS": 1,
			"natLang-MAX_NUM_FORMS": 1000,
			"natLang-0-nativeLang": "en",
			"natLang-1-nativeLang": "es",
		}

		natLangsForms = NatLangFormset(postData, {}, prefix=u"natLang")
		self.assertTrue(natLangsForms.is_valid())

	def test_BaseLangFormSet_no_duplicate_langs(self):

		NatLangFormset = formset_factory(
							NativeLangForm, 
							min_num=1,
							validate_min=True, 
							extra=0,
							can_delete=True,
							formset=BaseLangFormSet,
		)

		postData = {
			"natLang-INITIAL_FORMS": 0,
			"natLang-TOTAL_FORMS": 2,
			"natLang-MIN_NUM_FORMS": 1,
			"natLang-MAX_NUM_FORMS": 1000,
			"natLang-0-nativeLang": "en",
			"natLang-1-nativeLang": "en",
		}

		natLangsForms = NatLangFormset(postData, {}, prefix=u"natLang")
		self.assertFalse(natLangsForms.is_valid())
		non_form_errors = natLangsForms.non_form_errors()
		self.assertTrue(DUPLICATE_LANG_MESS in non_form_errors)
