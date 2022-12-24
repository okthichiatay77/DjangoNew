from django.shortcuts import render
from . import models
# Create your views here.

def index_view(request):
    return render(request, 'blogs/index.html')


def blog_view(request):
    list_blog = models.Blog.objects.all()
    return render(request, 'blogs/blog.html', {'list_blog': list_blog})

def detail_blog_view(request, pk):
    blog = models.Blog.objects.get(pk=pk)
    return render(request, 'blogs/blog-detail.html', {'blog': blog})


def page_about_view(request):

    return render(request, 'page-about.html')


