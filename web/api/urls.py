from django.urls import path
from .views import TimeStepData

app_name = 'api'
urlpatterns = [
    # used to send data to use for AJAX calls, then make graphs with Chart.js
    path('<int:pk>/chart/data/', TimeStepData.as_view(), name="data"),
]
