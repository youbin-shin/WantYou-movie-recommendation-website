from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie
from django.db.models import Q # search 기능
from django.http import JsonResponse
from .forms import MovieForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import requests
from django.contrib import messages


def home(request):
    return render(request, 'movies/home.html')


def index(request):
    # 영화 검색 기능
    search_movies = None
    query = None
    search_movie_num = 0
    if 'q' in request.GET:
        query = request.GET.get('q')
        if query == '' :
            messages.warning(request, '검색창에 입력해주세요.')
        else:
            search_movies = Movie.objects.all().filter(Q(title__contains=query) | Q(original_title__contains=query))
            if search_movies:
                search_movie_num = len(search_movies)
            else:
                messages.warning(request, '검색된 영화가 없습니다.')
    user_like_movie_data = 0
    like_data_dict = 0
    sorted_data = 0
    sorted_data1 = ""
    sorted_data2 = ""
    if request.user.is_authenticated:
        user = request.user
        user_like_movie_data = user.like_movies.all()
        like_data_dict = {}
        lendata = len(user_like_movie_data)
        if lendata-1 >= 0:
            for movie in user_like_movie_data:
                for genre in movie.genres:
                    if genre in like_data_dict:
                        like_data_dict[genre] += 1
                    else:
                        like_data_dict[genre] = 1
    
        sorted_data = sorted(like_data_dict.items(), key = lambda x: x[1], reverse=True)
        if len(sorted_data)>= 2:
            sorted_data1 = sorted_data[0][0]
            sorted_data2 = sorted_data[1][0]
        elif len(sorted_data) == 1:
            sorted_data1 = sorted_data[0]
    
    movies = Movie.objects.filter().order_by('-vote_average')
    allmovies = Movie.objects.all().order_by('-popularity')
    usermovie1_2 = []
    usermovie1 = []
    usermovie2 = []
    if request.user.is_authenticated:
        if len(sorted_data)>= 2:
            cnt = 0
            for allmovie in allmovies:
                if (sorted_data1 in allmovie.genres) and (sorted_data2 in allmovie.genres) and cnt<5:
                    usermovie1_2.append(allmovie)
                    cnt = cnt + 1
        cnt = 0
        for allmovie in allmovies:
            for genre in allmovie.genres:
                if (sorted_data1 in genre) and cnt<13:
                    if allmovie not in usermovie1_2:
                        usermovie1.append(allmovie)
                        cnt = cnt + 1
        cnt = 0
        for allmovie in allmovies:
            for genre in allmovie.genres:
                if  (sorted_data2 in genre) and cnt<13:
                    if allmovie not in usermovie1_2:
                        usermovie2.append(allmovie)
                        cnt = cnt + 1
        
    if request.user.is_authenticated:
        if len(sorted_data)>= 2: 
            movies1 = usermovie1_2[:4]
            movies2 = usermovie1[:4]
            movies3 = usermovie2[:4]
        elif len(sorted_data)>0:
            movies1 = usermovie1[:4]
            movies2 = usermovie1[4:8]
            movies3 = usermovie1[8:12]
        else:
            movies1 = Movie.objects.filter().order_by('-popularity')[:4]
            movies2 = Movie.objects.filter().order_by('-popularity')[4:8]
            movies3 = Movie.objects.filter().order_by('-popularity')[8:12]
    else:
        movies1 = Movie.objects.filter().order_by('-popularity')[:4]
        movies2 = Movie.objects.filter().order_by('-popularity')[4:8]
        movies3 = Movie.objects.filter().order_by('-popularity')[8:12]
    if sorted_data:
        len_sorted_data = len(sorted_data)
    else:
        len_sorted_data = 0

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
        'search_movies': search_movies,
        'query': query,
        'search_movie_num': search_movie_num,
        'len_sorted_data': len_sorted_data,
        'sorted_data1': sorted_data1,
        'sorted_data2' : sorted_data2,
    }
    return render(request, 'movies/index.html', context)


def detail(request, movie_pk):
    movie = Movie.objects.get(pk=movie_pk)
    url = 'https://www.googleapis.com/youtube/v3/search'
    params = {
        'key': 'AIzaSyAIwfeGhM-GQoPGzI1aNx3ouwt7u1cAivg',
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



@login_required
def delete(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.user.is_superuser != 1:
        return redirect('movies:index')
    else:
        movie = Movie.objects.get(pk=movie_pk)
        movie.delete()
    return redirect('movies:index')


@login_required
def update(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.user.is_superuser != 1:
        return redirect('movies:index')
    if request.method == 'POST':
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movies:detail', movie.pk)
    else:
        form = MovieForm(instance=movie)
    context = {
        'form': form,
        'movie': movie,
    }
    return render(request, 'movies/form.html', context)


def movie_create(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            movie = form.save()
            return redirect('movies:detail', movie.pk)
        messages.warning(request, '다시 쓰세요.')
    else:
        form = MovieForm()
    context = {
        'form': form,
    }
    return render(request, 'movies/form.html', context)