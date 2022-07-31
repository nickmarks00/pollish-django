from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import path, include
import debug_toolbar

from pollish.playground import PlaygroundView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pollish/', include('pollish.urls')),
    path('core/', include('core.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('', TemplateView.as_view(template_name='index.html')),
    path('playground/', PlaygroundView.as_view(), name='playground-view')
]

# Add this media root only in production
# if settings.DEBUG:

# TODO - remove comment on line 19 once AWS S3 configured for production media

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
