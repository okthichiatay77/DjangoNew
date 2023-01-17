from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from analysis_SEO.analysis_data import handle_total
from . import models


# Create your views here.

def index_view(request):
    if request.method == 'POST':
        domain = request.POST['url']
        url = reverse('blog:seo_analysis', kwargs={'domain': str(domain)})

        return HttpResponseRedirect(url)

    return render(request, 'blogs/index.html')


def blog_view(request):
    list_blog = models.Blog.objects.all()
    return render(request, 'blogs/blog.html', {'list_blog': list_blog})


def detail_blog_view(request, pk):
    blog = models.Blog.objects.get(pk=pk)
    return render(request, 'blogs/blog-detail.html', {'blog': blog})


def page_about_view(request):
    return render(request, 'page-about.html')


def seo_analysis(request, domain):
    if request.method == 'POST':
        url = request.POST['url']
        context = handle_total(url)
        good = 0
        bad = 0
        for check in context:
            if context[check] == 'Pass':
                good += 1
            else:
                bad += 1
        return HttpResponseRedirect(reverse('blog:seo_analysis', kwargs={'domain': str(url)}))
    else:
        context = handle_total(domain)
        good = 0
        bad = 0
        for check in context:
            if context[check] == 'Pass':
                good += 1
            else:
                bad += 1

    context['good'] = good
    context['bad'] = bad
    context['total'] = bad + good


    return render(request, 'page-seo-analysis.html', context=context)


def analysis_AMP(request):
    return render(request, 'analysis_AMP.html')
