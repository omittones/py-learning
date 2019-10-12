from . import models
from django.contrib import admin

admin.site.register(models.Playlist)
admin.site.register(models.Song)
admin.site.register(models.SongSource)
