""" pw URL Configuration """
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView, TemplateView

urlpatterns = []

if settings.DEBUG:
    urlpatterns += static('/st/', document_root=settings.STATIC_ROOT)

urlpatterns += [
    # url(r'^admin/', admin.site.urls),
    url(r'^hello/', include('apps.hello.urls')),
    url(r'^/*$', TemplateView.as_view(template_name="index.html")),
    url(r'', include('apps.tktk.urls')),
]
