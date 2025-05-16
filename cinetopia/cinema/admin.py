from django.contrib import admin
from . import models


# Register your models here.
admin.site.register(models.Rating)
admin.site.register(models.Movie)
admin.site.register(models.MovieType)
admin.site.register(models.MovieGenre)
admin.site.register(models.MovieCountry)
admin.site.register(models.UserMovieList)
admin.site.register(models.Country)
admin.site.register(models.Genre)
