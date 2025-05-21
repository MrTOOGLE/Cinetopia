from django.db.models import Avg
from django.http import StreamingHttpResponse
from django.views.generic import ListView, DetailView

from cinema.models import Movie
from cinema.services import open_file


class HomeView(ListView):
    template_name = 'cinema/index.html'
    queryset = Movie.objects.filter(
        is_active=True
    ).annotate(
        avg_rating=Avg('ratings__rating')
    ).prefetch_related(
        'ratings',
        'genres',
    ).order_by(
        '-avg_rating'
    )[:20]
    context_object_name = 'movies'


class MovieDetailView(DetailView):
    template_name = 'cinema/movie_detail.html'
    queryset = Movie.objects.filter(
        is_active=True
    ).annotate(
        avg_rating=Avg('ratings__rating')
    ).prefetch_related(
        'ratings',
        'genres',
    )
    context_object_name = 'movie'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


def get_streaming_video(request, pk: int):
    file, status_code, content_length, content_range = open_file(request, pk)
    response = StreamingHttpResponse(file, status=status_code, content_type='video/mp4')
    response['Accept-Ranges'] = 'bytes'
    response['Content-Length'] = str(content_length)
    response['Cache-Control'] = 'no-cache'
    response['Content-Range'] = content_range

    return response