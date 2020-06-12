from django.shortcuts import render
from .models import Movie, Genre
from django.core.paginator import Paginator

# def carousel(request):
#     movies1 = Movie.objects.filter().order_by('-popularity')[:3]
#     movies2 = Movie.objects.filter().order_by('-popularity')[4:7]
#     movies3 = Movie.objects.filter().order_by('-popularity')[8:11]
#     context = {
#         'movies1' : movies1,
#         'movies2' : movies2,
#         'movies3' : movies3,
#     }
#     return render(request, 'movies/index.html', context)


def index(request):
    movies1 = Movie.objects.filter().order_by('-popularity')[:4]
    movies2 = Movie.objects.filter().order_by('-popularity')[4:8]
    movies3 = Movie.objects.filter().order_by('-popularity')[8:12]
    movies = Movie.objects.all()
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