from django.urls import path
from .views import HomePageView, AboutPageView, PostDetailsView, NewPostView, UpdatePostView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('post/new/', NewPostView.as_view(), name='post-new'),
    path('post/<int:post_id>/', PostDetailsView.as_view(), name='post-details'),
    path('post/<int:post_id>/edit', UpdatePostView.as_view(), name='post-edit')
]
