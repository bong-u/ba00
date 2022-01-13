from django.urls import path
from . import views

urlpatterns = [
    path('musician/', views.TestView.as_view())
]