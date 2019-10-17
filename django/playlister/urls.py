from django.urls import path
from . import views

urlpatterns = [
    path('<str:source>/', views.HomePageView.as_view(), name='home'),
    path('', views.HomePageView.as_view(), name='home', kwargs={'source': 'user'})
]
