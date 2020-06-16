from django.urls import path
from . import views


app_name = 'movies'

urlpatterns = [
    path('', views.home, name='home'),
    path('index/', views.index, name='index'), # homepage
    path('movie_create/', views.movie_create, name='movie_create'),
    path('<int:movie_pk>/detail/', views.detail, name='detail'),
    path('<int:movie_pk>/like/', views.like, name='like'),
    path('<int:movie_pk>/update/', views.update, name='update'),
    path('<int:movie_pk>/delete/', views.delete, name='delete'),
]

