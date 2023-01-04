from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns, static
from django.conf import settings
from . import views

urlpatterns = [
    path('', include('blogSEO.urls')),
    path('site/', include('SiteApp.urls')),
    path('admin/', admin.site.urls),
]

handler404 = "DjangoNew.views.page_not_found_view"

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
