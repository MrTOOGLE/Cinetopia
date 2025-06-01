from django.db.models import Avg, Q
from django.db.models.functions import Coalesce


class MovieFilter:
    FILTER_MAP = {
        'selected_genres': lambda qs, v: qs.filter(genres__name__in=v),
        'selected_types': lambda qs, v: qs.filter(type__in=v),
        'selected_year': lambda qs, v: qs.filter(release_year=v),
        'selected_country': lambda qs, v: qs.filter(countries__name=v),
        'search_query': lambda qs, v: qs.filter(
            Q(title__icontains=v) | Q(original_title__icontains=v)
        ),
    }

    @classmethod
    def apply_base_filters(cls, queryset):
        return queryset.filter(is_active=True).prefetch_related(
            'ratings', 'genres', 'countries'
        ).annotate(
            avg_rating=Coalesce(Avg('ratings__rating'), 0.0)
        )

    @classmethod
    def apply_custom_filters(cls, queryset, filters):
        for param, filter_function in cls.FILTER_MAP.items():
            if value := filters.get(param):
                queryset = filter_function(queryset, value)

        return queryset.filter(
            avg_rating__gte=filters.get('min_rating', 0),
            avg_rating__lte=filters.get('max_rating', 10)
        )
