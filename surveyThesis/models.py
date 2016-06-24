from django.db import models

from django.utils.translation import ugettext as _

class SurveyLine(models.Model):

	participantNumber = models.IntegerField()
	age = models.IntegerField()

	ED_NONE = 'none'
	ED_PRIMARY = 'primary'
	ED_SECONDARY = 'secondary'
	ED_UNDERGRAD = 'undergrad'
	ED_MASTER = 'master'
	ED_PHD = 'phd' 

	ED_CHOICES = (
		(ED_NONE, _()),
		(ED_PRIMARY, _(u'Elementary/Middle School')),
		(ED_SECONDARY, _(u'High school')),
		(ED_UNDERGRAD, _(u'Undergraduate')),
		(ED_MASTER, _(u'Master')),
		(ED_PHD, _(u'PhD')),
	)

	education = models.CharField(
		choices=ED_CHOICES,
	)
	date = models.DateTimeField(auto_now=True)
	
