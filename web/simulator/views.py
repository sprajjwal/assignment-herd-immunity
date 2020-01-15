from django.shortcuts import render
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import (FormView, CreateView, ModelFormMixin,
                                       UpdateView)
from simulator.models import Experiment, TimeStep
from simulator.forms import ExperimentForm
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect


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
