from django.contrib import admin
from .models import Genre, Movie, Comment, Community


admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(Community)
admin.site.register(Comment)