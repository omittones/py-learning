"""trading URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.urls import urlpatterns as auth_urlpatterns
from pages.urls import urlpatterns as pages_urlpatterns
from .views import AutoRedirectLoginView

authOverrides = list()
for p in auth_urlpatterns:
    if p.name == 'login':
        authOverrides.append(
            path('login/', AutoRedirectLoginView.as_view(), name='login'))
    # elif p.name == 'logout':
    #     authOverrides.append(path('logout/', OurLogoutView.as_view(), name='logout'))
    else:
        authOverrides.append(p)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(authOverrides)),  # app name, namespace
    path('', include(('playlister.urls', 'playlister'))),
    path('pages/', include(('pages.urls', 'pages')))
]
