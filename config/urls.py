from django.contrib import admin
from django.urls import path, include
from core.views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('accounts/', include('accounts.urls')),            # signup
    path('accounts/', include('django.contrib.auth.urls')), # login/logout/password
    path('catalog/', include('catalog.urls')),
    path('auctions/', include('auctions.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('', include('core.urls')),  # or wherever your home page is
]
