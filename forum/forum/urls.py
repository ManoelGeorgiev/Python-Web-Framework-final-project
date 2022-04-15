from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from forum import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('forum.accounts.urls')),
    path('', include('forum.main.urls')),
    path('tinymce/', include('tinymce.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
