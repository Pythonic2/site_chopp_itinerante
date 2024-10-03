from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import GaleriaView, GaleriaCreateView
urlpatterns = [
    path('galeria/',GaleriaView.as_view(), name='galeria'),
    path('cadastrar-fotos/',GaleriaCreateView.as_view(), name='cad_fotos')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
