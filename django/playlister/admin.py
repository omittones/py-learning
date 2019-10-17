from . import models
from django.contrib import admin
from django.urls import reverse
from django.http import HttpResponseRedirect


class PlaylistEntryInline(admin.StackedInline):
    model = models.PlaylistEntry
    fields = ['song']


class PlaylistAdmin(admin.ModelAdmin):
    inlines = [
        PlaylistEntryInline
    ]


class DeezerSettingsAdmin(admin.ModelAdmin):

    save_as = False
    save_as_continue = False

    def response_post_save_change(self, request, obj):
        post_url = reverse('admin:index', current_app=self.admin_site.name)
        return HttpResponseRedirect(post_url)

    def get_urls(self):
        urls = super().get_urls()
        return urls[0:1]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request):
        return self.change_view(request, '1')


admin.site.register(models.Playlist, PlaylistAdmin)
admin.site.register(models.Song)
admin.site.register(models.SongSource)
admin.site.register(models.DeezerSettings, DeezerSettingsAdmin)
