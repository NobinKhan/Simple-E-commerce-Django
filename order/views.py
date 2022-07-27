from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from cart.models import Item
from cart.models import Cart as Cartmodel
from order.models import  Order
from order.models import  Item as OrderItem
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import _get_queryset
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from sslcommerz_lib import SSLCOMMERZ
import uuid
# Create your views here.


class OrdersView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        if user.has_perm('order.view_order'):
            orders = Order.objects.filter(user=user)
            data = {
                'orders':orders,
            }
            return render(request, 'order/order.html', data)
        return render(request, 'order/order.html')
    
    def post(self, request):
        user = request.user
        if request.POST.get('cart_id'):
            cart = Cartmodel.objects.get(pk=request.POST.get('cart_id'))
            new_order = Order(
                user=user,
                bill_amount=cart.get_total_price(),
                transaction_id=uuid.uuid1()
            )
            new_order.save()
            items = Item.objects.filter(cart=cart)
            for item in items:
                order_new_item = OrderItem(
                    order=new_order,
                    product=item.product,
                    quantity=item.quantity,
                )
                order_new_item.save()
            cart.product.clear()
            messages.success(request, "Order Placed, make payment for approve")
            return redirect('orders')
        return HttpResponse("cart id not found")


class GetOrder(LoginRequiredMixin, View):  
    def post(self, request, order_id ):
        order = get_object_or_None(Order, pk=order_id)
        if order:
            items = OrderItem.objects.filter(order=order)
            data = {
                'order':order,
                'items':items,
            }
            return render(request, 'order/orderDetails.html', data)
        return Http404("Not Found")


class Payment(LoginRequiredMixin, View):
    sslsetting = { 
        'store_id': settings.STORE_ID, 
        'store_pass': settings.STORE_PASS, 
        'issandbox': settings.ISSANDBOX,
        }
    sslcz = SSLCOMMERZ(sslsetting)

    def post(self, request ):
        order_id = request.POST.get('order_id')
        order = get_object_or_None(Order, pk=order_id)
        product = order.product.all()
        user = request.user
        items = OrderItem.objects.filter(order=order)

        status_url = request.build_absolute_uri(reverse('complete'))

        post_body = {}
        post_body['total_amount'] = order.bill_amount
        post_body['currency'] = "BDT"
        post_body['tran_id'] = order.transaction_id
        post_body['success_url'] = status_url
        post_body['fail_url'] = status_url
        post_body['cancel_url'] = status_url
        post_body['cus_name'] = user.username
        post_body['cus_email'] = user.email
        post_body['cus_phone'] = "01700000000"
        post_body['cus_add1'] = "customer address"
        post_body['cus_city'] = "Dhaka"
        post_body['cus_country'] = "Bangladesh"
        post_body['shipping_method'] = "NO"
        post_body['num_of_item'] = items.count()
        post_body['product_name'] = product
        post_body['product_category'] = "Test Category"
        post_body['product_profile'] = "general"
        response = self.sslcz.createSession(post_body) # API response
        return redirect(response['GatewayPageURL'])



@csrf_exempt
def complete(request):
    if request.method == 'POST' or request.method == 'post':
        payment_data = request.POST
        status = payment_data['status']
        amount = payment_data['store_amount']

        if status == 'VALID':
            tran_id = payment_data['tran_id']
            order = Order.objects.get(transaction_id=tran_id)
            order.payment_status = 'Success'
            order.paid_amount = amount
            order.order_status = 'Approved'
            order.save()
            messages.success(request, "Your Payment Completed Successfully!")
            return redirect('orders')
            # return HttpResponseRedirect(reverse('payment:purchase', kwargs={'val_id': val_id, 'tran_id': tran_id}))
        elif status == 'FAILED':
            messages.warning(request, "Your Payment Failed Please try again!")
            return render(request, 'payment/complete.html')




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