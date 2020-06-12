from django.urls import path
from . import views

app_name = 'communities'

urlpatterns = [
    path('', views.review_list, name='review_list'),
    path('new_review/', views.new_review, name='new_review'),
    path('<int:review_pk>/', views.review_detail, name='review_detail'),
    path('<int:review_pk>/update/', views.review_update, name='review_update'),
    path('<int:review_pk>/delete/', views.review_delete, name='review_delete'),
    path('<int:review_pk>/comments/', views.comments_create, name='comments_create'),
    path('<int:review_pk>/comments/<int:comment_pk>/delete/', views.comments_delete, name='comments_delete'),
]