from django_mysql.models import ListCharField
from django.db import models
from django.conf import settings

class Movie(models.Model):
    title = models.CharField(max_length=100)
    original_title = models.CharField(max_length=100)
    release_date = models.DateField()
    popularity = models.FloatField()
    vote_count = models.IntegerField()
    vote_average = models.FloatField()
    adult = models.BooleanField()
    overview = models.TextField()
    original_language = models.CharField(max_length=100)
    poster_path = models.CharField(max_length=200)
    backdrop_path = models.CharField(max_length=200)
    # genres = ArrayField(models.CharField(max_length=50), blank=True)
    genres = ListCharField(
        base_field=models.CharField(max_length=20),
        size=19,
        max_length=(19 * 21)  # 6 * 10 character nominals, plus commas
        )
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_movies')

