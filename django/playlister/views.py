from . import models
from . import services
from django.shortcuts import render
from django.views.generic import ListView


class HomePageContext():
    def __init__(self, entry):
        self.id = entry.id
        self.name = entry.name
        if getattr(self, 'songs', None):
            self.description = 'm '.join([str(s) for s in entry.songs[0:4]])
        else:
            self.description = ''


class HomePageView(ListView):
    queryset = models.Playlist.objects.as_simple_with_songs()
    template_name = 'playlister/home.html'
    context_object_name = 'playlists'

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        object_list = context.get('object_list')
        con = self.get_context_object_name(object_list)
        object_list = [HomePageContext(o) for o in object_list]
        if con is not None:
            context[con] = object_list
        return context
