from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Genre
from django.http import JsonResponse
from django.core.paginator import Paginator


def index(request):
    movies1 = Movie.objects.filter().order_by('-popularity')[:4]
    movies2 = Movie.objects.filter().order_by('-popularity')[4:8]
    movies3 = Movie.objects.filter().order_by('-popularity')[8:12]
    movies = Movie.objects.filter().order_by('-vote_average')
    paginator = Paginator(movies, 12) # 12개씩 자르겠다!
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'movies': movies,
        'page_obj': page_obj,
        'movies1' : movies1,
        'movies2' : movies2,
        'movies3' : movies3,
    }
    return render(request, 'movies/index.html', context)


def detail(request, movie_pk):
    movie = Movie.objects.get(pk=movie_pk)
    context = {
        'movie': movie,
    }
    return render(request, 'movies/detail.html', context)


def like(request, movie_pk):
    user = request.user
    movie = get_object_or_404(Movie, pk=movie_pk)

    if movie.like_users.filter(pk=user.pk).exists():
        movie.like_users.remove(user)
        liked = False
    else:
        movie.like_users.add(user)
        liked = True

    context = {
        'count' : movie.like_users.count(),
        'liked' : liked,
    }
    return JsonResponse(context)