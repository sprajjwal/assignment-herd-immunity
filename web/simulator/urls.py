from django.urls import path
from .views import (
    ExperimentCreate,
    ExperimentDetail,
    ExperimentList,
    show_about_page,
)

app_name = 'simulator'
urlpatterns = [
    path('', ExperimentList.as_view(), name="list"),
    path('add-experiment/', ExperimentCreate.as_view(),
         name='simulation_creator'),
    path('about/', show_about_page, name='about'),
    path('<int:pk>/', ExperimentDetail.as_view(), name='experiment_detail'),
]
