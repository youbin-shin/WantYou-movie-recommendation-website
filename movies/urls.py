from django.urls import path
from . import views


app_name = 'movies'

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'), # homepage
    path('<int:movie_pk>/detail/', views.detail, name='detail'),
    path('<int:movie_pk>/like/', views.like, name='like'),
    # path('<int:movie_pk>/update/', views.update, name='update'),
    # path('<int:movie_pk>/delete/', views.delete, name='delete'),
]
