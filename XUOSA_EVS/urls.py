from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='evs/', permanent=True)),
    path('evs/', include('evs_app.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
