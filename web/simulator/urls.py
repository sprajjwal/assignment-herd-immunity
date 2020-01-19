from django.urls import path
from .views import (
    ExperimentCreate,
    ExperimentDetail,
    ListTimeStepData
)

app_name = 'simulator'
urlpatterns = [
    path('', ExperimentCreate.as_view(), name='simulation_creator'),
    path('<int:pk>/api/chart/data', ListTimeStepData.as_view()),  # used for Chart.js
    path('<int:pk>/', ExperimentDetail.as_view(), name='experiment_detail'),
]
