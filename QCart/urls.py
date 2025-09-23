from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')), #recorded the ip address and number of attempts for unethical access by abc person.
    path('sadlog/', admin.site.urls),
    path('', include('QuickCart.urls')),
    path('store/', include('store.urls')),
    path('cart/', include('carts.urls')),
    path('accounts/', include('accounts.urls')),
    path('orders/', include('orders.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
