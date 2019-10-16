from . import models
from . import services
from django.shortcuts import render
from django.views.generic import ListView


class HomePageContext():
    def __init__(self, *args, **kwargs):
        entry = args[0] if args else None
        self.id = entry.id if entry else kwargs.get('id', None)
        self.name = entry.name if entry else kwargs.get('name', None)
        if entry is not None and getattr(entry, 'songs', None):
            self.description = ', '.join([str(s) for s in entry.songs[0:4]])
        else:
            self.description = kwargs.get('description', '')


class HomePageView(ListView):
    template_name = 'playlister/home.html'
    context_object_name = 'playlists'

    def get_queryset(self):
        return models.Playlist.objects.as_simple_with_songs()

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        object_list = context.get('object_list')
        con = self.get_context_object_name(object_list)
        object_list = [HomePageContext(o) for o in object_list]
        context['object_list'] = object_list
        if con is not None:
            context[con] = object_list
        return context
