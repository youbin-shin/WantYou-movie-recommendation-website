from django.db import models
from django.conf import settings

# Create your models here.
class Review(models.Model):
    title = models.CharField(max_length=100, help_text='글의 제목을 작성해주세요.')
    movie_title = models.CharField(max_length=30, help_text='글에 관련된 영화를 작성해주세요.')
    rank = models.IntegerField(help_text='순위를 매겨주세요! 총 10점만점')
    content = models.TextField(help_text='내용을 작성해주세요.')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Comment(models.Model):
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)