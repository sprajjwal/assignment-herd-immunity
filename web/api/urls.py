from django.urls import path
from .views import ListTimeStepData

app_name = 'api'
urlpatterns = [
    # used to send data to use for AJAX calls, then make graphs with Chart.js
    path('<int:pk>/chart/data', ListTimeStepData.as_view(), name="data"),
]
