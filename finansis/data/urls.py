from django.urls import path
from .views import read_input

app_name = "data"

urlpatterns = [
    path('upload/', read_input, name='upload'),
]
