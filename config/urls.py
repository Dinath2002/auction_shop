# config/urls.py
from django.contrib import admin
from django.urls import path, include

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
]
