from django.views.generic import TemplateView, ListView
from .models import Post

class HomePageView(ListView):
    template_name = 'home.html'
    model = Post
    context_object_name = 'posts' # used in template to reference list of Posts

class AboutPageView(TemplateView):
    template_name = 'about.html'