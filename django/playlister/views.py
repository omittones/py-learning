from . import models
from . import services
from django import http
from django.shortcuts import render
from django.views.generic import ListView
from services.for_deezer import DeezerOAuthSettings


class HomePageView(ListView):
    template_name = 'playlister/home.html'
    context_object_name = 'playlists'
    source = 'local'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.source = kwargs.get('source', self.source)

    def get_queryset(self):
        provider = services.DataProvider.resolve(self.source)
        return provider.playlist_overview()

    def get(self, request, *args, **kwargs):

        if self.source == 'deezer':
            settings = next(iter(models.DeezerSettings.objects.all()[:1]))  # pylint: disable=no-member
            if not settings.access_token:
                oauth = DeezerOAuthSettings()
                oauth.app_id = settings.app_id
                oauth.app_secret = settings.app_secret
                url = oauth.request_access_code_url()
                return http.HttpResponseRedirect(redirect_to=url)

        return super().get(request, *args, **kwargs)

    # def get_context_data(self, object_list=None, **kwargs):
    #     context = super().get_context_data(object_list=object_list, **kwargs)
    #     object_list = context.get('object_list')
    #     con = self.get_context_object_name(object_list)
    #     object_list = [services.PlaylistViewModel(o) for o in object_list]
    #     context['object_list'] = object_list
    #     if con is not None:
    #         context[con] = object_list
    #     return context


def deezer_receive_code_view(request, *args, **kwargs):

    settings = next(iter(models.DeezerSettings.objects.all()[:1]))  # pylint: disable=no-member
    oauth = DeezerOAuthSettings()
    oauth.app_id = settings.app_id
    oauth.app_secret = settings.app_secret

    code = request.GET.get('code', None)
    if code:
        token = oauth.get_access_token(code)
        settings.access_token = token
        settings.save()
        return http.HttpResponseRedirect(redirect_to='/deezer')

    return http.HttpResponseRedirect(redirect_to='/')
