from django.urls import path
from .views import (
    ExperimentCreate,
    ExperimentDetail,
    show_about_page,
)

app_name = 'simulator'
urlpatterns = [
    path('', ExperimentCreate.as_view(), name='simulation_creator'),
    path('about/', show_about_page, name='about'),
    path('<int:pk>/', ExperimentDetail.as_view(), name='experiment_detail'),
]
