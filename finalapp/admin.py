"""
Program: models.py
Author: Tom Sorteberg
Last date modified: 12/17/2020

The admin file for the finalapp.  Determines options
available in the admin interface.
"""
from django.contrib import admin
from .models import Choice, Question
""" Class ChoiceInLIne"""


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


""" Class QuestionAdmin """


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')

    list_filter = ['pub_date']
    search_fields = ['question_text']


# Register classes with admin interface.
admin.site.register(Question, QuestionAdmin)
