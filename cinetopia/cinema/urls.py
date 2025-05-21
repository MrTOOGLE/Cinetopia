from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('movies/', views.MoviesView.as_view(), name='movies'),
    path('movies/search/', views.movie_search, name='movie_search'),
    path('movies/<slug:slug>/', views.MovieDetailView.as_view(), name='movie_detail'),
    path('movies/<int:pk>/stream/', views.get_streaming_video, name='movie-stream'),
]
