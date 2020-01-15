from django.urls import path
from .views import (
    ExperimentCreate,
)

app_name = 'simulator'
urlpatterns = [
    path('', ExperimentCreate.as_view(), name='simulation_creator'),
]
