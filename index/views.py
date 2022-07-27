from django.shortcuts import render, HttpResponse
from product.models import Product
from cart.models import Cart

# Create your views here.
def homepage(request):
    products = Product.objects.order_by('-id').filter(status=True)
    cart = Cart.objects.all()
    # products = None
    data = {
        'products':products,
    }
    response = render(request,'pages/index.html',data)
    return HttpResponse(response)