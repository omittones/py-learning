from . import models
from . import services
from django.shortcuts import render
from django.views.generic import ListView


class HomePageContext():
    def __init__(self, *args, **kwargs):
        playlist = args[0] if args else None
        self.id = playlist.id if playlist else kwargs.get('id', None)
        self.name = playlist.name if playlist else kwargs.get('name', None)
        if playlist is not None:
            self.description = playlist.describe()
        else:
            self.description = kwargs.get('description', '')


class HomePageView(ListView):
    template_name = 'playlister/home.html'
    context_object_name = 'playlists'

    def get_queryset(self):
        return models.Playlist.objects.with_description()

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        object_list = context.get('object_list')
        con = self.get_context_object_name(object_list)
        object_list = [HomePageContext(o) for o in object_list]
        context['object_list'] = object_list
        if con is not None:
            context[con] = object_list
        return context
