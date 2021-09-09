"""
Program: models.py
Author: Tom Sorteberg
Last date modified: 12/17/2020

The models controller for the finalapp.
"""
import datetime
from django.db import models
from django.utils import timezone


""" Class Question"""


class Question(models.Model):
    # Instance variable declaration and initialization.
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        """
        Default to string function.
        """
        # Return statement.
        return self.question_text

    def was_published_recently(self):
        """
        Function that determines if a Question object was created
        within the last 24 hours.  Returns a datetime object.
        """
        # Local variable declaration and initialization.
        now = timezone.now()
        # Return statement.
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    # Variables used to generate admin view of Question objects.
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


""" Class Choice """


class Choice(models.Model):
    # Instance variable declaration and initialization.
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """
        Default to string function.
        """
        # Return statement.
        return self.choice_text
