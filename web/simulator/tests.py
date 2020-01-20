from django.test import TestCase
from django.test.client import RequestFactory
from .models import Experiment, TimeStep
from django.urls import reverse
from .views import (
    ExperimentCreate,
    ExperimentDetail,
    ExperimentList,
    show_landing,
    show_about_page,
)


class ExperimentCreateTests(TestCase):
    '''A user experiments with simulation conditions on the site.'''
    pass


class ExperimentListTests(TestCase):
    '''A user sees the experiments ran by other users.'''
    pass


class ExperimentDetailTests(TestCase):
    '''A user sees in-depth information about the epidemic they simulated.'''
    pass


class LandingAndAboutPageTests(TestCase):
    '''Users view information about why the site exists, and what it does.'''
    pass
