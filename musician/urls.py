from django.urls import path
from . import views

urlpatterns = [
    path('', views.TestView.as_view()),
    path('search/', views.SearchView.as_view())
]