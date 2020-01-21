from django.test import TestCase
from django.test.client import RequestFactory
from simulator.models import Experiment, TimeStep
from django.urls import reverse
from simulator.views import (
    ExperimentCreate,
    ExperimentDetail,
    ExperimentList,
    show_landing,
    show_about_page,
)


class ExperimentCreateTests(TestCase):
    '''A user experiments with simulation conditions on the site.'''
    def setUp(self):
        '''Instaniate RequestFactory and User to make requests.'''
        self.factory = RequestFactory()


class ExperimentListTests(TestCase):
    '''A user sees the experiments ran by other users.'''
    def setUp(self):
        '''Instaniate RequestFactory and User to make requests.'''
        self.factory = RequestFactory()


class ExperimentDetailTests(TestCase):
    '''A user sees in-depth information about the epidemic they simulated.'''
    def setUp(self):
        '''Instaniate RequestFactory and User to make requests.'''
        self.factory = RequestFactory()


class LandingAndAboutPageTests(TestCase):
    '''Users view information about why the site exists, and what it does.'''
    def setUp(self):
        '''Instaniate RequestFactory and User to make requests.'''
        self.factory = RequestFactory()

    def get_landing_page(self):
        '''A site visitor is able to see the landing page of the site.'''
        request = self.factory.get('simulator:home')
        response = show_landing()(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Doubtful About Vaccines?')
