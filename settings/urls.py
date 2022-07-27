from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

admin.site.site_header = 'Ecom administration'
admin.site.site_title = 'Ecom Admin Panel'
admin.site.index_title = 'Ecom Management System'

urlpatterns = [
    path('', include('index.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('account.urls')),
    path('product/', include('product.urls')),
    path('cart/', include('cart.urls')),
    path('order/', include('order.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
