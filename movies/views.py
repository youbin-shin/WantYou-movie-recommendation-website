from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie
from django.http import JsonResponse
from django.db.models import Q # search 기능
from django.core.paginator import Paginator
import requests

def home(request):
    return render(request, 'movies/home.html')


def index(request):
    user_like_movie_data = 0
    like_data_dict = 0
    if request.user.is_authenticated:
        user = request.user
        user_like_movie_data = user.like_movies.all()
        like_data_dict = {}
        lendata = len(user_like_movie_data)
        sorted_data = 0
        if lendata-1 >= 0:
            for movie in user_like_movie_data:
                for genre in movie.genres:
                    if genre in like_data_dict:
                        like_data_dict[genre] += 1
                    else:
                        like_data_dict[genre] = 1
    
    sorted_data = sorted(like_data_dict.items(), key = lambda x: x[1], reverse=True)
    
     # 영화 검색 기능
    search_movies = None
    query = None
    if 'q' in request.GET:
        query = request.GET.get('q')
        search_movies = Movie.objects.all().filter(Q(title__contains=query) | Q(original_title__contains=query))
    search_movie_num = len(search_movies)

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
        'user_like_movie_data': user_like_movie_data,
        'like_data_dict' : like_data_dict,
        'sorted_data':sorted_data,
        'search_movies': search_movies,
        'query': query,
        'search_movie_num': search_movie_num
    }
    return render(request, 'movies/index.html', context)


def detail(request, movie_pk):
    movie = Movie.objects.get(pk=movie_pk)
    url = 'https://www.googleapis.com/youtube/v3/search'
    params = {
        'key': 'AIzaSyBbJVfbqE7deJZJGeI32ehYHCTEWxAQ9r0',
        'part': 'snippet',
        'type': 'video',
        'q': movie.original_title  + 'trailer',
    }
    response = requests.get(url, params)
    response_dict = response.json()
    # response_dict = response_dict['items']
    youtube_items = response_dict['items']
    # youtube_items = response_dict.id
    videoid = youtube_items[2]['id']['videoId']
    context = {
        'youtube_items': youtube_items,
        'movie': movie,
        'videoid': videoid,
        'response': response,

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