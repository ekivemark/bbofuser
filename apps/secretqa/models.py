"""
bbofuser: secretqa
FILE: models
Created: 8/4/15 10:39 AM

Create Secret Questions and Answers for a user
"""
__author__ = 'Mark Scrimshire:@ekivemark'

from django.db import models
from django.conf import settings


class QA(models.Model):
    """

    Create Per User Security Questions and Answers

    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    question_1 = models.CharField(max_length=2,
                                  choices = settings.SECURITY_QUESTION_CHOICES,
                                  blank=False)
    answer_1   = models.CharField(max_length=80, blank=False)
    question_2 = models.CharField(max_length=2,
                                  choices = settings.SECURITY_QUESTION_CHOICES,
                                  blank=False)
    answer_2   = models.CharField(max_length=80, blank=False)
    question_3 = models.CharField(max_length=80, blank=True)
    answer_3   = models.CharField(max_length=80, blank=True)
    question_4 = models.CharField(max_length=80, blank=True)
    answer_4   = models.CharField(max_length=80, blank=True)
    question_5 = models.CharField(max_length=80, blank=True)
    answer_5   = models.CharField(max_length=80, blank=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        created = self.date_created is None
        if not self.pk or created is None:
            if settings.DEBUG:
                print("Overriding Secret Q&A save")



        super(QA, self).save(*args, **kwargs)

    def __str__(self):
        return "%s %s's Record:%s" % (self.user.first_name,
                              self.user.last_name,
                              self.pk)



