from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Q
from django.db.models.functions import Coalesce
from django.http import StreamingHttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, TemplateView

from cinema.models import Movie, Genre, Country, Rating, UserMovieList
from cinema.services import open_file


class HomeView(TemplateView):
    template_name = 'cinema/index.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        base_queryset = Movie.objects.filter(
            is_active=True
        ).annotate(
            avg_rating=Avg('ratings__rating')
        ).prefetch_related(
            'ratings',
            'genres',
        )
        context_data['popular_movies'] = base_queryset.order_by('-avg_rating')[:15]
        context_data['new_movies'] = base_queryset.order_by('-release_year')[:15]

        return context_data


class MoviesView(ListView):
    template_name = 'cinema/movies.html'
    context_object_name = 'movies'
    paginate_by = 18
    sort_mapping = {
        '-rating': '-avg_rating',
        'rating': 'avg_rating',
        '-release_year': '-release_year',
        'release_year': 'release_year',
        'title': 'title',
        '-title': '-title'
    }

    def get_queryset(self):
        base_queryset = self._get_base_queryset()
        filtered_queryset = self._apply_filters(base_queryset)

        return self._apply_sorting(filtered_queryset)

    def _get_base_queryset(self):
        query = self.request.GET.get('query', '')
        base_queryset = Movie.objects.filter(is_active=True)
        if query:
            base_queryset = base_queryset.filter(title__icontains=query)
        base_queryset = base_queryset.prefetch_related(
            'ratings',
            'genres',
            'countries',
        ).annotate(
            avg_rating=Coalesce(
                Avg('ratings__rating'),
                0.0,
            )
        )
        return base_queryset

    def _apply_filters(self, queryset):
        selected_genres = self.request.GET.getlist('genre')
        selected_types = self.request.GET.getlist('type')
        selected_year = self.request.GET.get('year')
        selected_country = self.request.GET.get('country')
        rating_range = self.request.GET.get('rating', '0,10')
        min_rating, max_rating = map(float, rating_range.split(','))

        if selected_genres:
            queryset = queryset.filter(genres__name__in=selected_genres)
        if selected_types:
            queryset = queryset.filter(type__in=selected_types)
        if selected_year:
            queryset = queryset.filter(release_year=selected_year)
        if selected_country:
            queryset = queryset.filter(countries__name=selected_country)

        return queryset.filter(
            avg_rating__gte=min_rating,
            avg_rating__lte=max_rating
        )

    def _apply_sorting(self, queryset):
        selected_sort = self.request.GET.get('sort', '-rating')
        return queryset.order_by(self.sort_mapping.get(selected_sort, '-avg_rating'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        request = self.request
        rating_range = request.GET.get('rating', '0,10')
        min_rating, max_rating = map(float, rating_range.split(','))
        selected_year = request.GET.get('year', '')
        context.update({
            'genres': Genre.objects.all(),
            'countries': Country.objects.all(),
            'years': self._get_available_years(),
            'content_types': Movie.CONTENT_TYPES,
            'selected_genres': request.GET.getlist('genre'),
            'selected_types': request.GET.getlist('type'),
            'selected_year': int(selected_year) if selected_year.isdigit() else 0,
            'selected_country': request.GET.get('country'),
            'min_rating': min_rating,
            'max_rating': max_rating,
            'selected_sort': request.GET.get('sort', '-rating'),
        })
        return context

    @staticmethod
    def _get_available_years():
        return Movie.objects.filter(
            is_active=True
        ).order_by(
            '-release_year'
        ).values_list(
            'release_year',
            flat=True
        ).distinct()


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'user_rating': Rating.objects.filter(
                movie=self.object,
                user=self.request.user
            ).first(),
            'list_types': UserMovieList.LIST_TYPES
        })
        return context

def get_streaming_video(request, pk: int):
    file, status_code, content_length, content_range = open_file(request, pk)
    response = StreamingHttpResponse(file, status=status_code, content_type='video/mp4')
    response['Accept-Ranges'] = 'bytes'
    response['Content-Length'] = str(content_length)
    response['Cache-Control'] = 'no-cache'
    response['Content-Range'] = content_range

    return response


def movie_search(request):
    query = request.GET.get('query', '')
    if query:
        movies = Movie.objects.filter(
            Q(title__icontains=query) &
            Q(is_active=True)
        ).prefetch_related('genres')[:10]

        results = [{
            'title': movie.title,
            'slug': movie.slug,
            'poster': movie.poster.url if movie.poster else '',
            'release_year': movie.release_year
        } for movie in movies]
    else:
        results = []

    return JsonResponse({'movies': results})


@require_POST
@login_required
def rate_movie(request):
    movie_id = request.POST.get('movie_id')
    rating = request.POST.get('rating')

    try:
        movie = Movie.objects.get(pk=movie_id)
        rating = int(rating)

        if rating < 1 or rating > 10:
            return JsonResponse({'success': False, 'error': 'Оценка должна быть от 1 до 10'})

        Rating.objects.update_or_create(
            movie=movie,
            user=request.user,
            defaults={'rating': rating}
        )

        return JsonResponse({'success': True})

    except Movie.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Фильм не найден'})
    except ValueError:
        return JsonResponse({'success': False, 'error': 'Некорректная оценка'})
