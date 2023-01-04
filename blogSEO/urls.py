from django.urls import path
from . import views


app_name = 'blog'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('blog/', views.blog_view, name='blog'),
    path('detail-blog/<int:pk>/', views.detail_blog_view, name='detail_blog'),
    path('page-about/', views.page_about_view, name='page_about'),
    path('seo-analysis/<str:domain>/', views.seo_analysis, name='seo_analysis'),
    path('analysis-amp/', views.analysis_AMP, name='analysis_amp'),
]