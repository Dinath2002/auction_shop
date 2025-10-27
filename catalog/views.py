from django.views.generic import ListView, DetailView
from .models import Product

class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    paginate_by = 12

class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
