from django.contrib import admin
from . import models


admin.site.register(models.Rating)
admin.site.register(models.Movie)
admin.site.register(models.MovieType)
admin.site.register(models.UserMovieList)
admin.site.register(models.Country)
admin.site.register(models.Genre)
