from functools import lru_cache
from django.urls import reverse
from django.http.response import HttpResponse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from .models import Post, CustomUser


class HomePageView(ListView):
    template_name = 'pages/home.html'
    model = Post
    context_object_name = 'posts'  # used in template to reference list of Posts

    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)
    #     context['users'] = users
    #     return context

    @property
    @lru_cache(maxsize=1)
    def extra_context(self):
        # convert to list to avoid reading QuerySet in template
        users = list(CustomUser.objects.with_nm_posts())
        return {'users': users}


class AboutPageView(TemplateView):
    template_name = 'pages/about.html'


class PostDetailsView(DetailView):
    template_name = 'pages/post_details.html'
    model = Post
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponse(status=200, content='')

    # def setup(self, *args, **kwargs):
    #     return super().setup(*args, **kwargs)
    # def get(self, request, *args, **kwargs):
    #     return super().get(request)


class NewPostView(CreateView):
    model = Post
    template_name = 'pages/post_new.html'
    fields = ['name', 'text', 'author']

    def get_success_url(self):
        return reverse('home')


class UpdatePostView(UpdateView):
    model = Post
    template_name = 'pages/post_edit.html'
    fields = ['name', 'text']
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'
