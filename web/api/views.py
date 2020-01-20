from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponseRedirect, JsonResponse
from .serializers import TimeStepSerializer
from simulator.models import Experiment, TimeStep


class TimeStepData(APIView):
    """
    View to list the fields and values of all time steps related to an
    Experiment.
    """
    serializer_class = TimeStepSerializer
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
        # get all Time Steps related to the Experiment, return the last
        time_step = (
            TimeStep.objects.filter(experiment__id=pk).order_by('pk').last()
        )
        population_size = time_step.alive + time_step.dead
        data = {
                "labels": [
                    "Dead",
                    "Alive - Vaccinated",
                    "Alive - Uninfected",
                    "Alive - No Interaction"
                ],
                "pop_sizes": [
                    time_step.dead,
                    time_step.total_vaccinated,
                    time_step.uninfected,
                    time_step.uninteracted
                ]
        }
        return Response(data)
