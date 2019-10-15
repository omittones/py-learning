from . import models
from django.shortcuts import render
from django.views.generic import ListView


class HomePageView(ListView):
    model = models.Playlist
    template_name = 'playlister/home.html'
    context_object_name = 'playlists'
