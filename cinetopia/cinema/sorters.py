class MovieSorter:
    SORT_MAPPING = {
        '-rating': '-avg_rating',
        'rating': 'avg_rating',
        '-release_year': '-release_year',
        'release_year': 'release_year',
        'title': 'title',
        '-title': '-title'
    }

    @classmethod
    def apply_sorting(cls, queryset, sort_key='-rating'):
        return queryset.order_by(cls.SORT_MAPPING.get(sort_key, '-avg_rating'))
