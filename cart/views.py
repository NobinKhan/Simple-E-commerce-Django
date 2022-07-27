from django.shortcuts import redirect, render
from django.views import View
from cart.models import Item
from cart.models import Cart as Cartmodel
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import _get_queryset
from product.models import Product
# Create your views here.




class CartView(LoginRequiredMixin, View):
    
    def get(self, request):
        user = request.user
        if user.has_perm('cart.view_cart'):
            items = Item.objects.filter(cart__user=user)
            # items = Cartmodel.objects.annotate(price=Sum(F('product__item__quantity') * F('product__new_price'))).get(user=request.user)
            # for item in items:
            #     item.product['price'] = item.product.new_price * item.quantity
            #     print(item.product.price)
            # print(f" price = {items.get_price()}")
            cart, _ = Cartmodel.objects.get_or_create(user=user)
            data = {
                'items':items,
                'cart':cart,
            }
            return render(request, 'cart/cart.html', data)
        return render(request, 'cart/cart.html')
    
    def post(self, request):
        user = request.user
        if request.POST.get('deleteproductid'):
            product = Product.objects.get(pk=request.POST['deleteproductid'])
            item = Item.objects.get(cart__user=user, product=product)
            item.delete()
            messages.warning(request, "Item Successfully deleted from your cart")
            return redirect('cart')
        else:
            product = Product.objects.get(pk=request.POST['product_id'])
            item = get_object_or_None(Item, cart__user=user, product=product)
            if item:
                item.quantity = item.quantity + 1
                item.save()
                messages.success(request, "Item Successfully added to your cart")
                return redirect('cart')
            else:
                cartInstance, _ = Cartmodel.objects.get_or_create(user=user)
                newItem = Item(
                    cart=cartInstance,
                    product=product,
                    quantity=1,
                )
                newItem.save()
                messages.success(request, "Item Successfully added to your cart")
                return redirect('cart')




def get_object_or_None(klass, *args, **kwargs):
    """
    Uses get() to return an object or None if the object does not exist.
    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the get() query.
    Note: Like with get(), a MultipleObjectsReturned will be raised if more than one
    object is found.
    """
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None