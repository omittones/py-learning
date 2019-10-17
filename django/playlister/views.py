from . import models
from . import services
from django.shortcuts import render
from django.views.generic import ListView


class HomePageView(ListView):
    template_name = 'playlister/home.html'
    context_object_name = 'playlists'

    def get_queryset(self):
        source = self.kwargs.get('source')
        provider = services.DataProvider.resolve(source)
        return provider.playlist_overview()

    # def get_context_data(self, object_list=None, **kwargs):
    #     context = super().get_context_data(object_list=object_list, **kwargs)
    #     object_list = context.get('object_list')
    #     con = self.get_context_object_name(object_list)
    #     object_list = [services.PlaylistViewModel(o) for o in object_list]
    #     context['object_list'] = object_list
    #     if con is not None:
    #         context[con] = object_list
    #     return context
