from django.urls import path

from . import views

urlpatterns =[
    path('<int:flat_id>', views.product_details, name='product'),
    
]
