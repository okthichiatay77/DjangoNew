from django.shortcuts import render
from . import models
from django.http.response import HttpResponseRedirect
from django.urls import reverse

from analysis_SEO.analysis_data import handle_total
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
    url_img, title, desc, canonical, robot, revisit_after, content_lang, meta_content_type, viewport, heading, iframe, link_external, favicon, check_sitemap = handle_total(domain)
    return render(request, 'page-seo-analysis.html', {'url_img': url_img, 'canonical': canonical,
                                                      'title': title, 'heading': heading,
                                                      'desc': desc, 'r_iframe': iframe,
                                                      'list_link_external': link_external, 'favicon': favicon, 'robot': robot,
                                                      'revisit_after': revisit_after, 'content_language': content_lang,
                                                      'meta_content_type': meta_content_type, 'viewport': viewport,
                                                      'check_sitemap': check_sitemap})

