
from django.contrib import admin
from .import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
    path('cart/', include('cart.urls')),
    path('payment/', include('payment.urls')),
    
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
