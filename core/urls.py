from django.urls import path
from .views import HomeView    # make sure this import exists

app_name = "core"

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]
