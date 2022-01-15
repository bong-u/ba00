from django.urls import path
from . import views

urlpatterns = [
    path('', views.MusicianView.as_view()),
    
    path('update/', views.UpdateView.as_view()),
    path('search/', views.SearchView.as_view()),
    path('add/', views.AddMusicianView.as_view())
]