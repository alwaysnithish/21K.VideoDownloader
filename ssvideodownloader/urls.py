from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('aboutus/', views.aboutus, name='aboutus'),
  
    path('privacypolicy/',views.privacypolicy,name='privacypolicy'),
    path('termsandconditions/',views.termsandconditions,name='termsandconditions'),

    # Serve ads.txt
    re_path(r'^sitemap\.xml$', serve, {'document_root': settings.STATIC_ROOT, 'path': 'sitemap.xml'}),
    re_path(r'^ads\.txt$', serve, {'document_root': settings.STATIC_ROOT, 'path': 'ads.txt'}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
