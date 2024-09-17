from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('', include('authentication.urls')),
    path('', include('produto.urls')),
    path('', include('carrinho.urls')),
    path('', include('pagamento.urls')),
    path('', include('testemunho.urls')),
]
