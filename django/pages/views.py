from django.urls import reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from .models import Post

class HomePageView(ListView):
    template_name = 'home.html'
    model = Post
    context_object_name = 'posts' # used in template to reference list of Posts


class AboutPageView(TemplateView):
    template_name = 'about.html'


class PostDetailsView(DetailView):
    template_name = 'post_details.html'
    model = Post
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    # def get(self, request, *args, **kwargs):
    #     return super().get(request)


class NewPostView(CreateView):
    model = Post
    template_name = 'post_new.html'
    fields = ['name', 'text', 'author']


class UpdatePostView(UpdateView):
    model = Post
    template_name = 'post_edit.html'
    fields = ['name', 'text']