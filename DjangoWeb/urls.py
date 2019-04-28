"""DjangoWeb URL Configuration

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
from django.urls import path
from django.conf.urls import url
from blog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^login/',views.login),
    url(r'^welcome/',views.welcome),
    url(r'^logout/',views.logout),
    url(r'^test$',views.Test.as_view()),
    url(r'^formtest$',views.formtest),

    url(r'^pages/', views.pages),
    url(r'^django_pages/',views.django_pages),
    url(r'^django_pages_plus/',views.django_pages_plus),

    url(r'^form_part/',views.form_part),

]
