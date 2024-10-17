from django.urls import path
from .views import IndexView, GaleriaView, GaleriaCreateView,FeedbackView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('galeria/',GaleriaView.as_view(), name='galeria'),
    path('cadastrar-fotos/',GaleriaCreateView.as_view(), name='cad_fotos'),
    path('feedback/',FeedbackView.as_view(), name='feedback')

    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
