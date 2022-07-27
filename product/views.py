from .models import Product
from django.shortcuts import get_object_or_404, render

# Create your views here.
def product_details(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    context = {
    'product': product
    }
    return render(request, 'listings/listing.html', context)