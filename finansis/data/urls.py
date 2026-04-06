from django.urls import path
from .views import read_input, graphs_data

app_name = "data"

urlpatterns = [
    path('upload/', read_input, name='upload'),
    path('graphics/', graphs_data, name='graphics'),
]
