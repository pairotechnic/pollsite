'''
    Purpose : Defines the paths to each view in the polls app
    Author : Rohit Pai
    Date : 10th July 2024

    NOTE : 
    To access a view in a browser, we need to map it to a URL - 
    and for this we need to define a URL configuration, or “URLconf” for short. 
    These URL configurations are defined inside each Django app, 
    and they are Python files named urls.py.
'''

# Standard Library Import

# Third Party Import
from django.urls import path

# Local Application Imports
from . import views

app_name = "polls"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote")
]