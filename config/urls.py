# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Built-in auth views: login, logout, password reset, etc.
    path('accounts/', include('django.contrib.auth.urls')),

    # Your custom signup view
    path('accounts/', include('accounts.urls')),

    # Your site URLs
    path('', include('core.urls')),
    path('catalog/', include('catalog.urls')),
    path('auctions/', include('auctions.urls')),
    path('cart/', include('cart.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
