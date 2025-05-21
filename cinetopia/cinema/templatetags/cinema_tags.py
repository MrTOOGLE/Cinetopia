from django import template

register = template.Library()

@register.inclusion_tag('cinema/tags/movie_carousel.html')
def movie_carousel(movies, title):
    return {
        'movies': movies,
        'title': title
    }
