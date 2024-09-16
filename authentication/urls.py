from django.urls import path
from .views import logout_view,LoginUsuario,RegisterUser,EventoView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUsuario.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('cadastrar-evento/', EventoView.as_view(), name='cad-evento'),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)