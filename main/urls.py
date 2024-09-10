from django.urls import path
from .views import home,simple_test,create_payment_link
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),
    path('pag/', simple_test, name='pag'),
    path('create-payment-link/', create_payment_link, name='create_payment_link'),

    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
