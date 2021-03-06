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
        '''Instaniate RequestFactory to make requests.'''
        self.factory = RequestFactory()

    def test_getting_create_page(self):
        '''Site visitor sees the form to add an Experiment.'''
        request = self.factory.get('simulator:simulation_creator')
        response = ExperimentCreate.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please fill out the form below.')

    def test_submitting_create_form(self):
        '''A site visitor adds a new Experiment.'''
        # data inputted by visitor into the form
        title = 'Ebola Outbreak'
        form_data = {
            'title': title,
            'population_size': 1000,
            'vaccination_percent': 0.98,
            'virus_name': 'Ebola',
            'mortality_chance': 0.98,
            'reproductive_rate': 0.09,
            'initial_infected': 12
        }
        request = self.factory.post('simulator:simulation_creator', form_data)
        response = ExperimentCreate.as_view()(request)
        # a new Experiment is inserted in the db
        new_experiment = Experiment.objects.get(title=title)
        self.assertTrue(new_experiment, not None)
        # the visitor is redirected
        self.assertEqual(response.status_code, 302)


class ExperimentListTests(TestCase):
    '''A user sees the experiments ran by other users.'''
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

    def test_getting_list_page(self):
        '''A site visitor can see Experiment instances already in the db.'''
        request = self.factory.get('simulator:list')
        response = ExperimentList.as_view()(request)
        self.assertEqual(response.status_code, 200)
        # the page has the correct header
        self.assertContains(response, 'Past Simulations')
        # the page correctly displays the number of Experiments in the db
        self.assertContains(response, '(1)')
        # the page hs the appropriate info about the Experiment instance
        self.assertContains(response, 'Ebola Outbreak')


class ExperimentDetailTests(TestCase):
    '''A user sees in-depth information about the epidemic they simulated.'''
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

    def test_get_details_for_one_experiment(self):
        '''Site visitor sees more nuanced data about an Experiment instance.'''
        id = self.experiment.id
        request = self.factory.get(f'/{id}/')
        response = ExperimentDetail.as_view()(request, id)
        # the response carries a 200 status
        self.assertEqual(response.status_code, 200)
        # the correct content appears on the page
        self.assertContains(response, 'And the Results Are In!')
        # there is a row whose step id matches that of an actual TimeStep
        time_step_id = (
            TimeStep.objects.filter(experiment=self.experiment).last().step_id
        )
        self.assertContains(response, f'<th scope="row">{time_step_id}</th>')


class LandingAndAboutPageTests(TestCase):
    '''Users view information about why the site exists, and what it does.'''
    def setUp(self):
        '''Instaniate RequestFactory to make requests.'''
        self.factory = RequestFactory()

    def get_landing_page(self):
        '''A site visitor is able to see the landing page of the site.'''
        request = self.factory.get('simulator:home')
        response = show_landing()(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Doubtful About Vaccines?')

    def get_about_page(self):
        '''A site vistor is able to see the About section of the site.'''
        request = self.factory.get('simulator:about')
        response = show_about_page()(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,
                            'Why Should You Care About Herd Immunity?')
