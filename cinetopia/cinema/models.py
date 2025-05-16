from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator, MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Country(models.Model):
    name = models.CharField(unique=True, max_length=100)


class MovieCountry(models.Model):
    movie = models.ForeignKey('Movie', models.CASCADE)
    country = models.ForeignKey('Country', models.CASCADE)

    class Meta:
        unique_together = (('movie', 'country'),)


class Genre(models.Model):
    name = models.CharField(unique=True, max_length=50)


class MovieGenre(models.Model):
    movie = models.ForeignKey('Movie', models.CASCADE)
    genre = models.ForeignKey('Genre', models.CASCADE)

    class Meta:
        unique_together = (('movie', 'genre'),)


class MovieType(models.Model):
    CONTENT_TYPES = [
        ('movie', 'Фильм'),
        ('series', 'Сериал'),
        ('cartoon', 'Мультфильм'),
        ('anime', 'Аниме'),
        ('documentary', 'Документальный'),
        ('tv_show', 'ТВ-шоу'),
    ]

    name = models.CharField(
        max_length=20,
        choices=CONTENT_TYPES,
        unique=True
    )


class Movie(models.Model):
    CONTENT_TYPES = [
        ('movie', 'Фильм'),
        ('series', 'Сериал'),
        ('cartoon', 'Мультфильм'),
        ('anime', 'Аниме'),
        ('documentary', 'Документальный'),
        ('tv_show', 'ТВ-шоу'),
    ]

    title = models.CharField(max_length=255)
    original_title = models.CharField(max_length=255, blank=True, null=True)
    release_year = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    poster = models.ImageField(
        upload_to='posters/',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])],
        blank=True,
        null=True
    )
    movie_file = models.FileField(
        upload_to='movies/',
        validators=[FileExtensionValidator(['mp4', 'mkv', 'webm'])],
        blank=True,
        null=True
    )
    duration = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=20, choices=CONTENT_TYPES)
    added_by = models.ForeignKey(User, models.CASCADE, blank=True, null=True)
    added_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    genres = models.ManyToManyField('Genre', related_name='movies', through='MovieGenre')
    countries = models.ManyToManyField('Country', related_name='movies', through='MovieCountry')


class Rating(models.Model):
    movie = models.ForeignKey('Movie', models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, models.CASCADE, related_name='ratings')
    rating = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(1), MaxValueValidator(10)])

    class Meta:
        unique_together = (('movie', 'user'),)


class UserMovieList(models.Model):
    LIST_TYPES = [
        ('watched', 'Просмотрено'),
        ('watching', 'Просматривается'),
        ('delayed', 'Отложено'),
        ('abandoned', 'Брошено'),
        ('favorite', 'Избранное'),
    ]
    user = models.ForeignKey(User, models.CASCADE, related_name='lists')
    movie = models.ForeignKey('Movie', models.CASCADE, related_name='lists')
    list_type = models.CharField(max_length=20, choices=LIST_TYPES)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('user', 'movie'),)
