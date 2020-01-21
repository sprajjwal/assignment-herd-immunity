from django.test import TestCase
from rest_framework.test import (
    APIRequestFactory, APITestCase
)
from rest_framework import status
from django.urls import reverse
from wiki.models import Experiment, TimeStep
from api.serializers import ExperimentSerializer, TimeStepSerializer
from api.views import TimeStepData


class TimeStepDataTests(TestCase):
    """
    This endpoint returns data about the final TimeStep related to an
    Experiment.
    """
    def setUp(self):
        '''Instaniate RequestFactory and User to make requests.'''
        self.factory = RequestFactory()
