from django.contrib import admin
from django.urls import path, include
from django.conf import settings # new
from  django.conf.urls.static import static #new
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('authentication.urls')),
    path('', include('main.urls')),
    path('', include('pagamento.urls')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)