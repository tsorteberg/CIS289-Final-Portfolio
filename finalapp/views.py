"""
Program: views.py
Author: Tom Sorteberg
Last date modified: 12/17/2020

The controller file for rendering views for the finalapp.
"""
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource
from bokeh.palettes import Category20c
from bokeh.transform import cumsum
import pandas as pd
from math import pi

from .models import Choice, Question


""" Class IndexView"""


class IndexView(generic.ListView):

    # Instance variable declaration and initialization.
    template_name = 'finalapp/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Function that lists the last 5 questions entered into the system.
        """
        # Return statement.
        return Question.objects.filter(pub_date__lte=
                                       timezone.now()).order_by('-pub_date')[:5]


""" Class DetailView"""


class DetailView(generic.DetailView):

    # Instance variable declaration and initialization.
    model = Question
    template_name = 'finalapp/detail.html'

    def get_queryset(self):
        """
        Function that returns the question objects to be listed in the
        Detail view.
        """
        # Return statement.
        return Question.objects.filter(pub_date__lte=timezone.now())


""" Class ResultsView"""


class ResultsView(generic.DetailView):

    # Instance variable declaration and initialization.
    model = Question
    template_name = 'finalapp/results.html'


def vote(request, question_id):
    """
    Function that returns the Vote view.
    """
    # Local variable declaration and initialization.
    question = get_object_or_404(Question, pk=question_id)
    # Try except clause for input validation.  If no value has been entered,
    # then an error message is displayed to the user.
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Reload Vote view.
        return render(request, 'finalapp/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        # Update database.
        selected_choice.votes += 1
        selected_choice.save()
        # Prevents user from entering redundant data from hitting the
        # back button.
        # Return statement.
        return HttpResponseRedirect(reverse('finalapp:results',
                                            args=(question.id,)))


def bar_chart(request):
    """
    Function that renders a view with a bar chart summarizing
    all Choice object data.
    """
    # Local variable declaration and initialization.
    x_list = []
    y_list = []
    # Output all Choice object data to a dictionary.
    output = Choice.objects.all().values()
    # Input dictionary into Pandas dataframe and remove redundant columns.
    my_frame = pd.DataFrame(output)
    my_frame.drop('id', axis='columns', inplace=True)
    my_frame.drop('question_id', axis='columns', inplace=True)
    # Export data from data frame to two lists.
    for index, rows in my_frame.iterrows():
        x_list.append(rows.choice_text)
        y_list.append(rows.votes)
    # Define vertical bar chart.
    p = figure(x_range=x_list, title="Choices by Popularity.")
    p.vbar(x=x_list, top=y_list, width=0.8)
    # Function call to render bar chart view.
    scripts, divs = components(p)
    # Return statement.
    return render(request, "finalapp/chart.html", {"the_scripts": scripts, "the_divs": divs})


def pie_chart(request):
    """
    Function that renders a view with a pie chart summarizing
    all Choice object data.
    """
    # Local variable declaration and initialization.
    pie_dict = {}
    # Output all Choice object data to a dictionary.
    output = Choice.objects.all().values()
    # Input dictionary into Pandas dataframe and remove redundant columns.
    my_frame = pd.DataFrame(output)
    my_frame.drop('id', axis='columns', inplace=True)
    my_frame.drop('question_id', axis='columns', inplace=True)
    # Build new dictionary from Pandas dataframe.
    for index, rows in my_frame.iterrows():
        pie_dict[rows.choice_text] = rows.votes
    # Create new dictionary and format output for pie chart.
    data = pd.Series(pie_dict).reset_index(name='value').rename(columns={'index':'choice'})
    data['angle'] = data['value']/data['value'].sum() * 2*pi
    data['color'] = Category20c[len(pie_dict)]
    # Define pie chart.
    p = figure(plot_height=350, title="Pie Chart", toolbar_location=None,
               tools="hover", tooltips="@country: @value", x_range=(-0.5, 1.0))
    p.wedge(x=0, y=1, radius=0.4,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', legend_field='choice', source=data)
    p.axis.axis_label = None
    p.axis.visible = False
    # Function call to render pie chart view.
    scripts, divs = components(p)
    # Return statement.
    return render(request, "finalapp/chart.html", {"the_scripts": scripts, "the_divs": divs})



