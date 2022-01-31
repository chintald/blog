"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from core import views
from . import views

#for post's generic views
from .views import PostCreateView, PostUpdateView, PostDeleteView

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.HomeView, name='HomeView'),
    # path('post/<pk>/<slug:slug>', PostView.as_view(), name='PostView'),
    # path('bridge/', views.bridge, name='bridge'),
    
    path('<post_id>/post_detail/', views.post_detail, name='post_detail'),
    
    #For Post Operations

    path('post/create/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
]
