from django.test import TestCase
from rest_framework.test import (
    APIRequestFactory, APITestCase
)
from rest_framework import status
from django.urls import reverse
from simulator.models import Experiment, TimeStep
from api.serializers import ExperimentSerializer, TimeStepSerializer
from api.views import TimeStepData


class TimeStepDataTests(APITestCase):
    """
    This endpoint returns data about the final TimeStep related to an
    Experiment.
    """
    def setUp(self):
        '''Instaniate RequestFactory and Experiment objects to use in tests.'''
        self.factory = RequestFactory()
        # Experiment object to use for tests
        self.experiment = Experiment.objects.create(title='Ebola Outbreak',
                                                    population_size=1000,
                                                    vaccination_percent=0.98,
                                                    virus_name='Ebola',
                                                    mortality_chance=0.98,
                                                    reproductive_rate=0.09,
                                                    initial_infected=12)
        self.experiment.save()
        # generate the related TimeStep instances as well
        self.experiment.run_experiment()
        # capture the related TimeStep as an attirbute
        unordered_time_steps = (
            TimeStep.objects.filter(experiment=self.experiment)
        )
        ordered_time_steps = time_steps.order_by('step_id')
        self.time_step = ordered_time_steps.last()

    def test_getting_json_response(self):
        '''The data returned about the TimeStep is accurate.'''
        pass
