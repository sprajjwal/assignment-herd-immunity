from django.shortcuts import render
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, CreateView, ModelFormMixin
from simulator.models import Experiment, TimeStep
from simulator.forms import ExperimentForm
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response


class ExperimentCreate(CreateView):
    '''User is able to make a new experiment on the system.'''
    model = Experiment
    form_class = ExperimentForm
    template_name = 'simulator/index.html'

    def form_valid(self, form, *args, **kwargs):
        '''Adds model instances to the db as appropriate.'''
        self.object = form.save()
        self.object.run_experiment()
        return HttpResponseRedirect(self.get_success_url())


class ExperimentDetail(DetailView):
    '''Displays a page with results of a specific experiment.'''
    model = Experiment
    template_name = 'simulator/results.html'

    def get(self, request, pk):
        """Renders a page to show the boarding instructions for a single Trip.

           Parameters:
           request(HttpRequest): the GET request sent to the server
           pk(int): unique id value of an Experiment instance

           Returns:
           HttpResponse: the view of the detail template

        """
        experiment = self.get_queryset().get(pk=pk)
        time_steps = TimeStep.objects.filter(experiment=experiment)
        context = {
            'experiment': experiment,
            'time_steps': time_steps
        }
        return render(request, self.template_name, context)


class ListTimeStepData(APIView):
    """
    View to list the fields and values of all time steps related to an
    Experiment.
    """
    authentication_classes = list()
    permission_classes = list()

    def get(self, request, pk, format=None):
        """Return a list of all time steps with fields and values.

           request(HttpRequest): the GET request sent to the server
           pk(int): unique id value of an Experiment instance
           format(str): the suffix applied to the endpoint to indicate how the
                        data is structured (i.e. html, json)

           Returns:
           HttpResponse: the view of the detail template
        """
        experiment = Experiment.objects.get(pk=pk)
        time_steps = TimeStep.objects.filter(experiment=experiment)
        data = {
            "experiment": {
                "title": experiment.title,
                "population_size": experiment.population_size,
                "vaccination_percent": experiment.vaccination_percent,
                "virus_name": experiment.virus_name,
                "mortality_chance": experiment.mortality_chance,
                "reproductive_rate": experiment.reproductive_rate,
                "initial_infected": experiment.initial_infected
            },
            "time_steps": [
                {
                    "": 9
                } for time_step in time_steps]
        }
        return Response(data)
