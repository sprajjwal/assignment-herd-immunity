from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponseRedirect, JsonResponse
from .serializers import TimeStepSerializer
from simulator.models import Experiment, TimeStep


class ListTimeStepData(APIView):
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
        time_steps = TimeStep.objects.filter(experiment__id=pk)
        data = {
            "time_steps": [
                {
                    "step_id": time_step.step_id,
                    "total_infected": time_step.total_infected,
                    "current_infected": time_step.current_infected,
                    "vaccinated_population": time_step.vaccinated_population,
                    "dead": time_step.dead,
                    "total_vaccinated": time_step.total_vaccinated,
                    "alive": time_step.alive,
                    "uninfected": time_step.uninfected,
                    "uninteracted": time_step.uninteracted
                } for time_step in time_steps
            ]
        }
        return Response(data)
