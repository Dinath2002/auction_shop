from django.urls import path
from . import views
app_name = 'auctions'
urlpatterns = [
    path('', views.ListingListView.as_view(), name='listing_list'),
    path('<int:pk>/', views.ListingDetailView.as_view(), name='listing_detail'),
    path('<int:pk>/bid/', views.place_bid, name='place_bid'),
    path('<int:pk>/buy-now/', views.buy_now, name='buy_now'),
]
