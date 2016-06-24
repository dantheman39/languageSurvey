#!/usr/bin/env python
#-*- coding: utf-8 -*-

from django.shortcuts import render
from forms import PageOne
import logging

logger = logging.getLogger(__name__)

def surveyPage(request):

	logger.info('Testing with one page for now')	

	if request.method == 'POST':
		form = PageOne(request.POST)

		if form.is_valid():
			logger.info('Add code to process data')

	else:
		form = PageOne()

	return render(request, 'one.html', {'form': form})
