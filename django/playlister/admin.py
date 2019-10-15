from . import models
from django.contrib import admin


class PlaylistEntryInline(admin.StackedInline):
    model = models.PlaylistEntry
    fields = ['song']


class PlaylistAdmin(admin.ModelAdmin):
    inlines = [
        PlaylistEntryInline
    ]


admin.site.register(models.Playlist, PlaylistAdmin)
admin.site.register(models.Song)
admin.site.register(models.SongSource)
