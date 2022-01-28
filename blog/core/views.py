from django.shortcuts import render, redirect,get_object_or_404
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

from core.models import Post

# Create your views here.

def home(request):
    context = {}
    return render(request, "base.html", context)

def HomeView(request):
    data = Post.objects.all()
    context = { 'data' : data }
    return render(request,"core/home.html", context)


def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    context = {'post' : post}
    return render(request, "core/post_detail.html", context)