from django.urls import path

from . import views

urlpatterns =[
    path('', views.OrdersView.as_view(), name='orders'),
    path('<int:order_id>', views.GetOrder.as_view(), name='order'),  
    path('payment/', views.Payment.as_view(), name='payment'),  
    path('status/', views.complete, name='complete'),  
]
