# accounts/views.py

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView


class SignupView(CreateView):
    """
    Simple signup view:
    - Uses Django's built-in UserCreationForm
    - Renders registration/signup.html
    - On success, redirects to the login page
    """
    form_class = UserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("accounts:login")
